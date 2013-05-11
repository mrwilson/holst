# Todo

* Objects: Host, Hostgroup, Service, Servicegroup
* Compilation

machine_name:
  type: host
  fqdn: machine_name.foo.bar
  ip: 1.2.3.4
  service:
    - http
    - ssh

host_group_name:
  - machine_1
  - machine_2

http:
  type: service
  

