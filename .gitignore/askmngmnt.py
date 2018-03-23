from flask import Flask, jsonify
from kubernetes import client, config

app = Flask(__name__)
config.load_kube_config()

@app.route('/servers')
def show_servers():
    resp = client.CoreV1Api()

    for i in resp.list_service_for_all_namespaces_with_http_info()[0].items:
        if i.status.load_balancer.ingress != None:
            mc = i
            pub_ip = mc.status.load_balancer.ingress[0].ip
            # print(i.status.load_balancer.ingress)

    mc_cluster = []
    ep = {}
    mc_node = {}



    for i in mc.spec.ports:
        # print(i)
        ept = {}
        ep[i.name] = pub_ip + ':' + str(i.port)
        #ep.append(ept)
        # print(ep)

    mc_node['name'] = mc.metadata.name
    mc_node['endpoints'] = ep
    mc_cluster.append(mc_node)

    #mc_cluster['endpoints'] = ept

    return jsonify(mc_cluster)


if __name__ == '__main__':
    app.run()


