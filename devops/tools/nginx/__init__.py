import yaml

def format(path, indent = 0):
    source = yaml.load(open(path))
    for domain in source['mapping']:
        # print('  domain : {domain}'.format(domain=domain['domain']))
        for port in domain['ports']:
            print('{indent}server {{'.format(indent=' '*indent))
            print('{indent}listen {port};'.format(indent=' '*(indent+4), port=port['port']))
            print('{indent}server_name {domain};'.format(indent=' ' * (indent + 4), domain=domain['domain']))
            # print('    port : {port}'.format(port=port['port']))
            for service in port['services']:
                print('{indent}location {location} {{'.format(indent=' ' * (indent + 4), location=service['location']))
                print('{indent}proxy_pass {redirect};'.format(indent=' ' * (indent + 8), redirect=service['redirect']))
                print('{indent}}}'.format(indent=' ' * (indent + 4), location=service['location']))
                pass
                # print(' service : {service}'.format(service=service.get('desc', service['redirect']).encode('utf-8')))

            print('{indent}}}'.format(indent=' ' * indent))

