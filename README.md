# Build the Docker application

```
docker build . -t disk_filler
```

# Run the Docker application

```
docker run  -d -p 8080:8080 --name filler disk_filler
```

# Login into the Docker container

```
docker run --rm -it -p 8080:8080 --name filler disk_filler sh
or
docker exec -it filler sh
```

# Managing the application

```
export CONTAINER_IP=172.17.0.2

Fill disk: curl $CONTAINER_IP>:8080/fill?size=2
Stop filling: curl $CONTAINER_IP:8080/stop
```

# Copying manually the Docker image to Vagrant DC/OS nodes

```
$ docker save disk_filler | bzip2 | pv | ssh -i /home/user/.vagrant.d/insecure_private_key vagrant@192.168.121.219 'bunzip2 | sudo docker load'
```

# Working with DC/OS Marathon

```
$ dcos marathon app add filler-ephimeral-docker.json
$ dcos marathon app list
ID                             MEM  CPUS  TASKS  HEALTH  DEPLOYMENT  WAITING CONTAINER  CMD  
/disk-filler-ephimeral-docker   32  0.25   1/1    N/A       ---      False   DOCKER     N/A

$ curl filler-docker.marathon.l4lb.thisdcos.directory:1234/fill?size=2
JID-1538137537.680487.3040
$ curl filler-docker.marathon.l4lb.thisdcos.directory:1234/stop
JID-1538137548.5942774.2521
```

Notes about Mesos UCR containers with native Docker images:

```
# cat /opt/mesosphere/etc/mesos-slave-common
[...]
MESOS_DOCKER_REGISTRY=/opt/
[...]
```

If the --docker_registry agent flag points to a local directory (e.g.,
/tmp/mesos/images/docker), the provisioner will pull Docker images from local
filesystem, assuming Docker archives (result of docker save) are stored there
based on the image name and tag. For example, the operator can put a
busybox:latest.tar (the result of docker save -o busybox:latest.tar busybox)
under /tmp/mesos/images/docker and launch the agent by specifying
--docker_registry=/tmp/mesos/images/docker. Then the framework can launch a
Docker container by specifying busybox:latest as the name of the Docker image.

Note that this option won't change the default registry server for Docker
containerizer. (default: https://registry-1.docker.io)

# Working with PVs in Apache Mesos

```
curl -XPOST http://leader.mesos:5050/master/reserve -d slaveId="6e8240cd-ca35-427f-a55c-1b31e55eba4c-S3" -H "Content-Type: application/json" -d resources='[{"name": "cpus", "type": "SCALAR", "scalar": { "value": 0.5 }, "role": "test" }]' -vvv

curl -XPOST http://leader.mesos:5050/master/reserve -d slaveId="6e8240cd-ca35-427f-a55c-1b31e55eba4c-S3" -H "Content-Type: application/json" -d resources='[{"name": "cpus", "type": "SCALAR", "scalar": { "value": 0.5 }, "role": "test"}, "reservation": {"principal": "open"}]' -vvv

curl -XPOST http://leader.mesos:5050/master/reserve -d slaveId="6e8240cd-ca35-427f-a55c-1b31e55eba4c-S3" -H "Content-Type: application/json" -d resources='[{"name": "cpus", "type": "SCALAR", "scalar": { "value": 0.5 }, "role": "test", "reservation": {"principal": "open"}}]' -vvv

curl -d @quota-test-role.json -X POST http://leader.mesos:5050/quota -vvv

curl -XPOST http://leader.mesos:5050/master/unreserve -d slaveId="6e8240cd-ca35-427f-a55c-1b31e55eba4c-S3" -H "Content-Type: application/json" -d resources='[{"name": "cpus", "type": "SCALAR", "scalar": { "value": 0.5 }, "role": "test", "reservation": {"principal": "open"}}]' -vvv

curl -X DELETE http://leader.mesos:5050/quota/test -vvv

curl -XPOST http://leader.mesos:5050/master/unreserve -d slaveId="6e8240cd-ca35-427f-a55c-1b31e55eba4c-S3" -H "Content-Type: application/json" -d resources='[{"name": "cpus", "type": "SCALAR", "scalar": { "value": 0.5 }, "role": "test", "reservation": {"principal": "open"}}]' -vvv

curl -XPOST http://leader.mesos:5050/master/reserve -d slaveId="6e8240cd-ca35-427f-a55c-1b31e55eba4c-S3" -H "Content-Type: application/json" -d resources='[{"name": "cpus", "type": "SCALAR", "scalar": { "value": 0.5 }, "role": "test", "reservation": {"principal": "open"}}]' -vvv

curl -d @quota-test-role.json -X POST http://leader.mesos:5050/quota -vvv

curl -X DELETE http://leader.mesos:5050/quota/test -vvv

curl -XPOST http://leader.mesos:5050/master/unreserve -d slaveId="6e8240cd-ca35-427f-a55c-1b31e55eba4c-S3" -H "Content-Type: application/json" -d resources='[{"name": "cpus", "type": "SCALAR", "scalar": { "value": 0.5 }, "role": "test", "reservation": {"principal": "open"}}]' -vvv

Listing quotas:

http://<master-IP>/mesos/quota

```

# How to create resources

```
cat /var/lib/dcos/mesos-resources | grep MESOS_RESOURCES | cut -d'=' -f2 | tr -d \' | jq .
[
  {
    "name": "ports",
    "type": "RANGES",
    "ranges": {
      "range": [
        {
          "begin": 1025,
          "end": 2180
        },
        {
          "begin": 2182,
          "end": 3887
        },
        {
          "begin": 3889,
          "end": 5049
        },
        {
          "begin": 5052,
          "end": 8079
        },
        {
          "begin": 8082,
          "end": 8180
        },
        {
          "begin": 8182,
          "end": 32000
        }
      ]
    }
  },
  {
    "name": "disk",
    "type": "SCALAR",
    "role": "*",
    "scalar": {
      "value": 35305
    }
  },
  {
    "name": "disk",
    "type": "SCALAR",
    "role": "disk_path01",
    "scalar": {
      "value": 2048
    },
    "disk": {
      "source": {
        "type": "PATH",
        "path": {
          "root": "/mnt/path01"
        }
      }
    }
  },
  {
    "name": "disk",
    "type": "SCALAR",
    "scalar": {
      "value": 10000
    },
    "disk": {
      "source": {
        "type": "PATH",
        "path": {
          "root": "/mnt/path02"
        }
      }
    }
  }
]
```

Note about disk resources availables:

```
curl <node-IP>:5051/state | jq .
{
	"version": "1.5.0",
	"git_sha": "0ba40f86759307cefab1c8702724debe87007bb0",
	"build_date": "2018-02-27 21:31:27",
	"build_time": 1519767087,
	"build_user": "",
	"start_time": 1538462281.18166,
	"id": "6e8240cd-ca35-427f-a55c-1b31e55eba4c-S7",
	"pid": "slave(1)@100.1.10.102:5051",
	"hostname": "100.1.10.102",
	"capabilities": [
		"MULTI_ROLE",
		"HIERARCHICAL_ROLE",
		"RESERVATION_REFINEMENT"
	],
	"resources": {
		"disk": 47353,
		"mem": 919,
		"gpus": 0,
		"cpus": 2,
		"ports": "[1025-2180, 2182-3887, 3889-5049, 5052-8079, 8082-8180, 8182-32000]"
	},
```

resources -> disk -> 47353 This is the total available disk this is the sum of

root disk "value": 35305 
+ 
path disk "/mnt/path01" value 2048
+ 
path disk "/mnt/path02" value 10000 
= 
47353

# Listing Reservations

Information about the reserved resources at each slave in the cluster can be
found by querying the /slaves master endpoint (under the
reserved_resources_full key).

The same information can also be found in the /state endpoint on the agent
(under the  reserved_resources_full key). The agent endpoint is useful to
confirm if a reservation has been propagated to the agent (which can fail in
the event of network partition or master/agent restarts).

At DC/OS deployment:

Master slaves state:

- With browser:
http://<master-IP>/mesos/slaves

- From whatever cluster node
curl -s leader.mesos:5050/slaves | jq .

Slave state:

- From browser:

http://<node-IP>:5051/state

- From whatever node:

curl <node-IP>:5051/state | jq .







