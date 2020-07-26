# !/bin/bash

# seta as colors do console
export TERM=xterm-256color

puts (){
    #tput sc
    echo -e "$(tput setaf 4) \U1F6C8  $1 $(tput sgr0)"
}

error () {
    #tput rc
    #tput el
    echo -e "$(tput setaf 1) \u2716  $1 $(tput sgr0)"
    exit 1
}   

success () {
    #tput rc
    #tput el 
    echo -e "$(tput bold)$(tput setaf 2) \u2713  $1  $(tput sgr0)"
}



load_config(){
  if [[ ! -e "config.json" ]]; then
    error "Missing ecs.config.json"
  fi
  CONFIG=`cat config.json | jq -r .`
}

if [[ ! `jq --help ` ]]; then
  error "JQ nao foi encontrado"
fi

if [[ -z "$1" ]]; then
    error "bash push.sh [STAGE=hml|prod]"
fi

[[ "$1" == "hml" ]] || [[ "$1" == "prod" ]] || error "STAGE invalido"

puts "Carregando Configuracoes"
CONFIG=
load_config

REGION="${AWS_DEFAULT_REGION}"
REPOSITORY=`echo "$CONFIG" | jq -r .projectName`

if [[ -z "$REGION" ]]; then
  error "Faltando setar o 'AWS_DEFAULT_REGION'"
fi

# setting image name
IMAGE_NAME="175572419266.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY:$1"
SERVICE_NAME="$REPOSITORY"-"$1"-service
CONTAINER_NAME="$REPOSITORY"-"$1"-container
TASK_NAME="$REPOSITORY"-"$1"-task
CLUSTER_NAME="$REPOSITORY"-"$1"
LOADBALANCER="$REPOSITORY"-"$1"-elb
TARGET_GROUP="$REPOSITORY"-"$1"-target

puts "REGION: $REGION"
puts "REPOSITORY: $REPOSITORY"
puts "SERVICE: $SERVICE_NAME"
puts "CLUSTER: $CLUSTER_NAME"
puts "TASK: $TASK_NAME"
puts "CONTAINER: $CONTAINER_NAME"
puts "IMAGE: $IMAGE_NAME"
puts "LOADBALANCER: $LOADBALANCER"


if [[ -z `aws ecr describe-repositories | grep "$REPOSITORY"` ]]; then
  puts "Criando Repositorio"
  if [[ ! `aws ecr create-repository --repository-name "$REPOSITORY"` ]]; then
    error "Error em criar o repositorio"
  fi
  success "Repositorio criado"  
fi

puts "Logando no docker"
eval $( aws ecr get-login --no-include-email --region "$REGION" )

puts "Criando Image"
docker build --build-arg stage="$1" -t "$REPOSITORY":"$1" .
success "Imagem criada"
docker tag "$REPOSITORY":"$1" "$IMAGE_NAME"
puts "Uploading image"
docker push "$IMAGE_NAME"
puts "IMAGEM ENVIADA"

# getting settings container
CPU=`echo $CONFIG | jq -r .cpu`
MEMORY=`echo $CONFIG | jq -r .memory`
PORTS=`echo $CONFIG | jq -r .portMappings`
DESIRED=`echo $CONFIG | jq -r .desiredCount`
SETTINGS=`echo $CONFIG | jq .settings."$1"`
ENVS=`echo $SETTINGS | jq .environments | jq 'to_entries | map( { name: .key, value: .value } )'`
CERTIFICATE=`echo $SETTINGS | jq -r '[ { CertificateArn: .certificateARN } ]'`
NETWORK=`echo $SETTINGS | jq '{ awsvpcConfiguration: .network }'`
GROUP=`echo $NETWORK | jq .awsvpcConfiguration.securityGroups | jq -r 'join(" ")'`
ELBSUBNETS=`echo $SETTINGS | jq -r .loadBalancer.subnets | jq -r 'join(" ")'`


CONTAINER='
{
    "executionRoleArn":"ecsTaskExecutionRole",
    "networkMode": "awsvpc",
    "family": "'$TASK_NAME'",
    "placementConstraints": [],
    "cpu": "'$CPU'",
    "memory": "'$MEMORY'",
    "volumes": [],
    "requiresCompatibilities": [
      "FARGATE"
    ],
    "containerDefinitions": [
      {
        "environment": '$ENVS',
        "name": "'$CONTAINER_NAME'",
        "mountPoints": [],
        "image": "'$IMAGE_NAME'",
        "cpu": '$CPU',
        "memory": '$MEMORY',
        "memoryReservation": '$MEMORY',
        "portMappings": '$PORTS',
        "logConfiguration": {
          "logDriver": "awslogs",
          "options": {
            "awslogs-group": "/ecs/first-run-task-definition",
            "awslogs-region": "'$REGION'",
            "awslogs-stream-prefix": "ecs"
          }
        },
        "entryPoint": [],
        "command": [],
        "essential": true,
        "volumesFrom": []
      }
    ]
}'

echo "$CONTAINER" > task.json

puts "Criando o task-definition"
if [[ ! `aws ecs register-task-definition --cli-input-json file://$PWD/task.json` ]]; then
    error "Falha criar o task definition"
fi
success "TASK-DEFITION criado"

if [[ -z `aws ecs list-clusters | grep "$SERVICE_NAME"` ]]; then
  puts "Criando o cluster"
  if [[ ! `aws ecs create-cluster --cluster-name "$CLUSTER_NAME"` ]]; then
    error "Falha em criar o cluster"
  fi
  success "CLUSTER criado"
else
  success "CLUSTER encontrado"
fi

puts "Procurando o load-balancer"

load_balancer=`aws elbv2 describe-load-balancers --name $LOADBALANCER`
if [[ ! $load_balancer  ]]; then
  puts "Criando load-balancer"
  load_balancer=`aws elbv2 create-load-balancer --name $LOADBALANCER --subnets $ELBSUBNETS --security-groups $GROUP` 
  if [[ ! load_balancer ]]; then
    error "Error para criar o load-balancer"
  fi
  success "Load balancer criado"
  
  loadARN=`echo $load_balancer | jq -r '.LoadBalancers | first | .LoadBalancerArn'`
  vpcID=`echo $load_balancer | jq -r .'LoadBalancers | first | .VpcId'`

  if [[ "$@" == *"--no-https"* ]]; then
    # para http
    puts "Criando target group HTTP"
    target=`aws elbv2 create-target-group --name $TARGET_GROUP --port 80 --protocol HTTP --target-type ip --vpc-id $vpcID --health-check-interval-seconds 180 --health-check-timeout-seconds 60`
    if [[ ! $target ]]; then
      error "Error ao criar target group"
    fi
    success "Target group criado"
    targetARN=`echo $target | jq -r '.TargetGroups | first | .TargetGroupArn'`
  
    puts "Criando listening"
    if [[ ! `aws elbv2 create-listener --load-balancer-arn $loadARN --protocol HTTP --port 80 --default-actions Type=forward,TargetGroupArn=$targetARN` ]]; then
      error "Error ao criar listening"
    fi
  else
    # para https
    puts "Criando target group HTTPS"
    target=`aws elbv2 create-target-group --name $TARGET_GROUP --port 80 --protocol HTTP --target-type ip --vpc-id $vpcID --health-check-interval-seconds 180 --health-check-timeout-seconds 60`
    if [[ ! $target ]]; then
      error "Error ao criar target group"
    fi
    success "Target group criado"
    targetARN=`echo $target | jq -r '.TargetGroups | first | .TargetGroupArn'`

    puts "Criando listening"
    echo "aws elbv2 create-listener --load-balancer-arn $loadARN --protocol HTTPS --port 443 --certificates $CERTIFICATE --ssl-policy ELBSecurityPolicy-FS-1-2-2019-08 --default-actions Type=forward,TargetGroupArn=$targetARN"
    if [[ ! `aws elbv2 create-listener --load-balancer-arn $loadARN --protocol HTTPS --port 443 --certificates "$CERTIFICATE" --ssl-policy ELBSecurityPolicy-FS-1-2-2019-08 --default-actions Type=forward,TargetGroupArn=$targetARN` ]]; then
      error "Error ao criar listening"
    fi
  fi

  success "Listening criado"
else
  success "Load balancer encontrado"
  loadARN=`echo $load_balancer | jq -r '.LoadBalancers | first | .LoadBalancerArn'`
  targetARN=`echo "$( aws elbv2 describe-target-groups --name $TARGET_GROUP )" | jq -r '.TargetGroups | first | .TargetGroupArn'`
fi

balancers=`echo '[
  {
    "targetGroupArn": "'$targetARN'",
    "containerName": "'$CONTAINER_NAME'",
    "containerPort": 80
  }
]'`

if [[ ! -z `aws ecs list-services --cluster "$CLUSTER_NAME" | grep "$SERVICE_NAME"` ]]; then
  puts "Atualizando o service"
  if [[ ! `aws ecs update-service --cluster "$CLUSTER_NAME" --service "$SERVICE_NAME" --task-definition "$TASK_NAME" --desired-count "$DESIRED" --force-new-deployment` ]]; then
    error "Falha ao atualizar o service"
  fi
  success "SERVICO atualizado"
else
  puts "Criando o service"
  if [[ ! `aws ecs create-service --cluster "$CLUSTER_NAME" --service-name "$SERVICE_NAME" --launch-type "FARGATE" --desired-count "$DESIRED" --network-configuration "$NETWORK" --task-definition "$TASK_NAME" --load-balancers "$balancers"` ]]; then
     error "Falha ao criar service"
  fi
  success "SERVICO criado"
fi
