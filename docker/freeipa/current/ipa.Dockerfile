# Dockerfile for freeipa servers
ARG centos_ver=centos7.6.1810
FROM centos:${centos_ver}
LABEL maintainer="<email>" \
version="1.0" \
purpose="test build freeipa on docker"
RUN groupadd -g 288 kdcproxy ; useradd -u 288 -g 288 -c 'IPA KDC Proxy User' -d '/var/lib/kdcproxy' -s '/sbin/nologin' kdcproxy && \
groupadd -g 289 ipaapi; useradd -u 289 -g 289 -c 'IPA Framework User' -r -d / -s '/sbin/nologin' ipaapi
RUN while yum check-update; do sleep 1; done && yum update -y
RUN yum install \
ntp \
bind-utils \
nc \
lsof \
net-tools \
expect -y
# wont need if volume bind works: RUN echo "server $(hostname -i | sed 's/.$/1/')" >> /etc/ntp.conf
RUN mkdir /root/ipa && \
touch /root/ipa/admin.pw && \
touch /root/ipa/directorymanager.pw
RUN yum install \
ipa-server \
ipa-server-dns \
ipa-server-trust-ad \
patch -y && \
yum clean all
ENV container oci
RUN ln -s /bin/false /usr/sbin/systemd-machine-id-setup && \
echo "DefaultLimitNOFILE=1024" >> /etc/systemd/system.conf
ENTRYPOINT ["/usr/sbin/init"]
STOPSIGNAL RTMIN+3
