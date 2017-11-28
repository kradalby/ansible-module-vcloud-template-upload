#!/usr/bin/python

__author__ = 'kradalby'

import os.path


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ovftool_path=dict(default="", type='str'),
            address=dict(required=True, type='str'),
            user=dict(required=True, type='str'),
            password=dict(required=True, type='str', no_log=True),
            virtual_datacenter=dict(required=True, type='str'),
            organization=dict(required=True, type='str'),
            catalog=dict(required=True, type='str'),
            template_name=dict(required=True, type='str'),
            ova_file=dict(required=True, type='str'),
            overwrite=dict(default=False, type='bool'),
            description=dict(default="", type='str')),
        supports_check_mode=True,
    )

    ovftool_exec = 'ovftool' if not module.params['ovftool_path'] else '{}/ovftool'.format(
        module.params['ovftool_path'])

    if not os.path.isfile(ovftool_exec):
        module.fail_json(
            msg='Could not find ovftool, is the path correct: {}?'.format(
                ovftool_exec))

    ova_file = module.params['ova_file']
    vcloud_string = 'vcloud://{}:{}@{}'.format(module.params['user'],
                                               module.params['password'],
                                               module.params['address'])

    template_string = '?vdc={}&org={}&vappTemplate={}&catalog={}'.format(
        module.params['virtual_datacenter'], module.params['organization'],
        module.params['template_name'], module.params['catalog'])
    command_tokens = [ovftool_exec]

    remote_path = vcloud_string + template_string

    command_tokens.extend([
        '--annotation="{}"'.format(module.params['description']),
        '--acceptAllEulas',
    ])

    if module.params['overwrite']:
        command_tokens.extend(['--overwrite'])

    command_tokens.extend([ova_file, remote_path])

    module.debug('Command tokens: {}'.format(command_tokens))
    print('PRINT Command tokens: {}'.format(command_tokens))

    ova_tool_result = module.run_command(command_tokens)

    if ova_tool_result[0] != 0:
        module.fail_json(
            msg='Failed to deploy OVA, error message from ovftool is: {}'.
            format(ova_tool_result[1]))

    module.exit_json(changed=True, ova_tool_result=ova_tool_result)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()