# Holst

A yaml-based dsl for iptables.

## Usage

    holst [options] templatefile hostname

## Options

    --accept-established  accept established connections by default
    --nat-header          add default nat rules to the rule file
    --loopback            allow loopback on input/output

## Host

    example_host:
        type: host
        ip: [1.2.3.4]
        input:
            ssh: [all]
        output:
            ssh: [other_host]

## Service

    ssh:
        type: service
        rules:
            - accept: ["tcp", 22]
            - reject: ["tcp", 9001]
