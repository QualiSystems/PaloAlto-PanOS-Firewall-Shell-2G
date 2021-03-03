from mock import patch, create_autospec
from cloudshell.shell.core.driver_context import ResourceCommandContext, ResourceContextDetails, \
    ReservationContextDetails
from driver import PaloAltoShellDriver as ShellDriver

set_vlan = "setVlan"
request1 = """{
  "driverRequest" : {
    "actions" : [{
      "connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
      "connectionParams" : {
        "vlanId" : "45",
        "mode" : "Access",
        "vlanServiceAttributes" : [{
          "attributeName" : "QnQ",
          "attributeValue" : "True",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "CTag",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Isolation Level",
          "attributeValue" : "Shared",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Access Mode",
          "attributeValue" : "Access",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "VLAN ID",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Virtual Network",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Pool Name",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }
        ],
        "type" : "setVlanParameter"
      },
      "connectorAttributes" : [],
      "actionId" : "457238ad-4023-49cf-8943-219cb038c0dc_4244579e-bf6f-4d14-84f9-32d9cacaf9d9",
      "actionTarget" : {
        "fullName" : "Router/Chassis 1/Module1/GigabitEhternet0-0-0-0",
        "fullAddress" : "192.168.28.150/1/1/1/7",
        "type" : "actionTarget"
      },
      "customActionAttributes" : [],
      "type" : "removeVlan"
    }
    ]
  }
}"""

request2 = """{
  "driverRequest" : {
    "actions" : [{
      "connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
      "connectionParams" : {
        "vlanId" : "45",
        "mode" : "Access",
        "vlanServiceAttributes" : [{
          "attributeName" : "QnQ",
          "attributeValue" : "True",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "CTag",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Isolation Level",
          "attributeValue" : "Shared",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Access Mode",
          "attributeValue" : "Access",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "VLAN ID",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Virtual Network",
          "attributeValue" : "876",
          "type" : "vlanServiceAttribute"
        }, {
          "attributeName" : "Pool Name",
          "attributeValue" : "",
          "type" : "vlanServiceAttribute"
        }
        ],
        "type" : "setVlanParameter"
      },
      "connectorAttributes" : [],
      "actionId" : "457238ad-4023-49cf-8943-219cb038c0dc_4244579e-bf6f-4d14-84f9-32d9cacaf9d9",
      "actionTarget" : {
        "fullName" : "Router/Chassis 1/Module1/GigabitEhternet0-0-0-0",
        "fullAddress" : "192.168.28.150/1/1/1/7",
        "type" : "actionTarget"
      },
      "customActionAttributes" : [],
      "type" : "setVlan"
    }
    ]
  }
}"""

SHELL_NAME = ShellDriver.SHELL_NAME + "."
# SHELL_NAME = ""

address = '192.168.26.24'
# address = '192.168.73.200'
# address = '192.168.73.5'
# address = '192.168.73.132'
# address = '192.168.73.152'
user = 'admin'
password = 'admin'
enable_password = ''
auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
api_port = 8029

context = create_autospec(ResourceCommandContext)
context.resource = create_autospec(ResourceContextDetails)
context.resource.name = 'Test PanOS'
context.resource.fullname = 'Test PanOS'
context.resource.family = 'CS_Firewall'
context.reservation = create_autospec(ReservationContextDetails)
context.reservation.reservation_id = 'test_id'
context.resource.attributes = {}
context.resource.attributes['{}User'.format(SHELL_NAME)] = user
context.resource.attributes['{}Password'.format(SHELL_NAME)] = password
context.resource.attributes['{}host'.format(SHELL_NAME)] = address
context.resource.attributes['{}Enable Password'.format(SHELL_NAME)] = enable_password
# context.resource.attributes['Port'] = port
# context.resource.attributes['Backup Location'] = 'tftp://172.25.10.96/AireOS_test'
# context.resource.attributes['{}Backup Location'.format(SHELL_NAME)] = 'ftp://junos:junos@192.168.85.47'
# context.resource.attributes['{}Backup Location'.format(SHELL_NAME)] = 'ftp://user:pass@172.29.128.11'
context.resource.attributes['{}Backup Location'.format(SHELL_NAME)] = '192.168.85.47'
context.resource.attributes['{}Backup Type'.format(SHELL_NAME)] = 'tftp'
context.resource.address = address
# context.connectivity = ConnectivityContext()
# context.connectivity.admin_auth_token = auth_key
# context.connectivity.server_address = '10.5.1.2'
# context.connectivity.cloudshell_api_port = api_port
# context.resource.attributes['{}SNMP Version'.format(SHELL_NAME)] = 'v2c'
# context.resource.attributes['{}SNMP Read Community'.format(SHELL_NAME)] = 'public'
context.resource.attributes['{}SNMP Version'.format(SHELL_NAME)] = 'v3'
context.resource.attributes['{}SNMP V3 User'.format(SHELL_NAME)] = 'quali'
context.resource.attributes['{}SNMP V3 Password'.format(SHELL_NAME)] = 'Password1'
context.resource.attributes['{}SNMP V3 Private Key'.format(SHELL_NAME)] = 'Password1'
context.resource.attributes['{}SNMP V3 Authentication Protocol'.format(SHELL_NAME)] = 'SHA'
context.resource.attributes['{}SNMP V3 Privacy Protocol'.format(SHELL_NAME)] = 'AES-128'
context.resource.attributes['{}CLI Connection Type'.format(SHELL_NAME)] = 'ssh'
# context.resource.attributes['{}CLI TCP Port'.format(SHELL_NAME)] = 17000
context.resource.attributes['{}Enable SNMP'.format(SHELL_NAME)] = 'False'
context.resource.attributes['{}Disable SNMP'.format(SHELL_NAME)] = 'False'
context.resource.attributes['{}Sessions Concurrency Limit'.format(SHELL_NAME)] = '1'

if __name__ == '__main__':
    res = dict(context.resource.attributes)

    driver = ShellDriver()
    driver.initialize(context)

    with patch('driver.CloudShellSessionContext') as get_api:
        api = type('api', (object,),
                   {'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()
        # get_api.return_value = api

        get_api.return_value.get_api.return_value = api
        print("*" * 20, "START", "*" * 20)
        discovery = driver.get_inventory(context)

        print(discovery)
        # print "*" * 20, "START", "*" * 20
        # print(driver.health_check(context=context))
        # print "*" * 20, "START", "*" * 20
        # # print driver.load_firmware(context=context, path="pp", vrf_management_name=None)
        # # print "*" * 20, "START", "*" * 20
        # print driver.ApplyConnectivityChanges(context=context, request=request2)
        # print "*" * 20, "START", "*" * 20
        # print driver.ApplyConnectivityChanges(context=context, request=request1)
        # print "*" * 20, "START", "*" * 20
        # print driver.run_custom_command(context=context, custom_command="show config running")
        # print "*" * 20, "START", "*" * 20
        # save_result = driver.save(context=context, folder_path="", configuration_type="running")
        # print "*" * 20, "START", "*" * 20
        # print driver.save(context=context, folder_path="", configuration_type="startup")
        # print(driver.save(context=context, folder_path="tftp://192.168.85.63", configuration_type="running", vrf_management_name=""))
        # print driver.save(context=context,
        #                   folder_path="scp://quali:Password1@192.168.42.102/home/quali/scp_folder/",
        #                   configuration_type="startup")
        # print(driver.save(context=context,
        #                   folder_path="scp://quali:Password1@192.168.42.102/home/quali/scp_folder/",
        #                   configuration_type="running",
        #                   vrf_management_name=""))
        # "scp export configuration from running-config.xml to quali:Password1@192.168.42.102:/home/quali/scp_folder/PanOS-startup-021220-075825"

        # print driver.restore(context=context,
        #                      path="tftp://{}/{}".format("192.168.85.27", "Test_PanOS-running-110918-163559"),
        #                      configuration_type="running",
        #                      restore_method="override")
        # print driver.restore(context=context,
        #                           path="tftp://172.29.128.16/Test_ASA-startup-300317-182734",
        #                           configuration_type="startup",
        #                           restore_method="append")
        # print driver.restore(context=context,
        #                           path="tftp://172.29.128.16/Test_ASA-running-300317-182729",
        #                           configuration_type="running",
        #                           restore_method="override")
        # print driver.restore(context=context,
        #                           path="tftp://172.29.128.16/Test_ASA-running-300317-182729",
        #                           configuration_type="running",
        #                           restore_method="append")

        # print response
        print("*" * 20, "FINISH", "*" * 20)
