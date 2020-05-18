mesos-execute \
        --master=m1:5050 \
        --containerizer=docker \
        --name=test \
        --docker_image=busybox \
        --volumes='[{"container_path":"/tmp/hosts", "host_path":"/etc/hosts", "mode":"RO"}]' \
        --command="cat /tmp/hosts && sleep 5"
