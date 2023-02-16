# Minecraft Server on Amazon ECS

This project consists of two CloudFormation stacks that can
be deployed via [`stk`](https://github.com/jwoffindin/stk).

* minecraft-server - deploys a spot-instance minecraft server
* discord-bot  - partially-completed Discord Bot to manage the server - so my son can (or ban 🤔) his friends.

## Minecraft server

1. Create config file as below
1. Create VPC stack `cfn deploy vpc dev`
1. Spin up minecraft `cfn deploy minecraft dev`.
1. You can stop it any time with `cfn deploy minecraft dev --var running=false`


```
# minecraft.yml
includes:
  - common

refs:
  vpc:

vars:
  vpc_id: "{{ refs.vpc.VpcId }}"
  subnets: "{{ refs.vpc.PublicSubnets.split(',') }}"

  # Java version (Examples include latest, adopt13, openj9, etc) Refer to tag descriptions
  # available here: https://github.com/itzg/docker-minecraft-server
  container_image: "itzg/minecraft-server:latest"

  ami: ami-053d0f9f12656ea46 # /aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id
  instance_type: t3.medium
  spot_price: 0.02
  running: true

  # Enable/Disable ECS Container Insights for ECS Cluster
  insights_enabled: false

  log_group: minecraft

  # If you have a hosted zone in Route 53 and wish to set a DNS record whenever
  # your Minecraft instance starts, supply the name of the record here
  # (e.g. minecraft.mydomain.com).
  fqdn: "minecraft.{{ hosted_zone }}."

  minecraft_options:
    # Examples include SPIGOT, BUKKIT, TUINITY, etc
    # Refer to tag descriptions available here: https://github.com/itzg/docker-minecraft-server
    type:

    # Op/Administrator Player names
    ops:

    # The game's difficulty; one of peaceful, easy, normal, hard
    difficulty: normal

    # Usernames of your friends
    whitelist:

    # Server minecraft version
    version: 1.19

    # Memory allocation
    memory: 1G

    # The seed used to generate the world
    seed: -6138929407156785189

    # Max number of players that can connect simultaneously (default 20)
    max_players:

    # Max view radius (in chunks) the server will send to the client (default 10)
    view_distance:

    # Game mode: creative, survival (default), adventure, spectator (v1.8+)
    mode:

    # Options: DEFAULT, FLAT, LARGEBIOMES, AMPLIFIED, CUSTOMIZED, BUFFET, BIOMESOP (v1.12-), BIOMESOPLENTY (v1.15+)
    level_type: DEFAULT

    # By default the log file will grow without limit. Set to true to use a rolling log strategy (true/false)
    enable_rolling_logs: true

    # Server's timezone.
    # Use the canonical name of the format: Area/Location (e.g. America/New_York)
    tz: Pacific/Auckland

environments:
  dev:
    vars:
      ssh_allowed_cidrs: []
      allowed_cidrs: []

tags:
  Application: minecraft
```


## Discord bot

Not in a working state, although it does integrate and serve requests -
just doesn't do anything with them.

Configuration:

```
---
includes:
  - common

refs:
  lambda_layers:
  minecraft_server:

vars:
  application: "Minecraft Bot"
  python_lambda_layer_arn: "{{ refs.lambda_layers.PythonLayerArn }}"
  api_endpoint: "discord.{{ hosted_zone }}"
  frontend_sg: "{{ refs.minecraft_server.IngressSecurityGroupId }}"
  autoscaling_group: "{{ refs.minecraft_server.AutoscalingGroupId }}"
  ecs_service_id: "{{ refs.minecraft_server.EcsServiceId }}"

environments:
  dev:
    vars:
      discord_public_key: PUBLIC_KEY
      discord_app_id: APP_ID

      discord_bot_token: BOT_TOKEN
```

The deploy with

```
cfn deploy discord-bot dev
```
