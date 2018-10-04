<p align="center">
<img src="https://github.com/QualiSystems/devguide_source/raw/master/logo.png"></img>
</p>

# **Palo Alto Firewall Shell**  

Release date: October 2018

Shell version: 1.0.0

Document version: 1.0.0

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [Typical Workflow and Scenarios](#typical-workflow-and-scenarios)
* [References](#references)
* [Release Notes](#release-notes)


# Overview
A shell integrates a device model, application or other technology with CloudShell. A shell consists of a data model that defines how the device and its properties are modeled in CloudShell, along with automation that enables interaction with the device via CloudShell.

### Firewall Shells
CloudShell's Firewall shells enable you to manage your Firewall device similar to your networking equipment but without connectivity. In CloudShell, a Firewall shell runs commands, such as Autoload, Load, and Save Configuration. 

### **Palo Alto Firewall Shell**
**Palo Alto Firewall Shell** provides you with management capabilities such as device structure discovery and power management for the **Palo Alto Firewall**. 

For more information on the **Palo Alto Firewall**, see the official **Palo Alto** product documentation.

### Standard version
**Palo Alto Firewall Shell 1.0.0** is based on the **cloudshell firewall standard 3.0.1**.

For detailed information about the shell’s structure and attributes, see the **cloudshell firewall standard 3.0.1**.(https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/firewall_standard.md) in GitHub.

### Supported OS
▪ **PanOS 8.1.0**

### Requirements

Release: **Palo Alto Firewall Shell 1.0.0**

* CloudShell 8.0 and above

### Data Model

The shell's data model includes all shell metadata, families, and attributes.

#### **[Device Name] Families and Models**

The [Device Name] families and models are listed in the following table:

|Family|Model|Description|
|:---|:---|:---|
||||
||||
||||
||||

#### **[Device Name] Attributes**

The attribute names and types are listed in the following table:

|Attribute|Type|Default value|Description|
|:---|:---|:---|:---|
|||||
|||||
|||||
|||||

### Automation
This section describes the automation (drivers or scripts) associated with the data model. The shell’s driver is provided as part of the shell package. There are two types of automation processes, Autoload and Resource. Autoload is executed when creating the resource in the Inventory dashboard, while resource commands are run in the Sandbox, providing that the resource has been discovered and is online.

|Command|Description|
|:-----|:-----|
|||
|||
|||
	
# Downloading the Shell
The **Palo Alto Firewall Shell 1.0.0** is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises:

|File name|Description|
|:---|:---|
|[Shell .zip File Name]|[Device Name] shell package|
|[Shell Offline Requirements .zip File Name]|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the **Palo Alto Firewall Shell 1.0.0** and configure and modify the shell’s devices.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page.
  
  2. In CloudShell Portal, as Global administrator, open the **Manage – Shells** page.
  
  3. Click **Import**.
  
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**.

The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

### Offline installation of a shell

**Note:** Offline installation instructions are relevant only if CloudShell Execution Server has no access to PyPi. You can skip this section if your execution server has access to PyPi. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder. The dependencies folder may differ, depending on the CloudShell version you are using:

* For CloudShell version 8.3 and above, see [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository).

* For CloudShell version 8.2, perform the appropriate procedure: [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository) or [Setting the python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

* For CloudShell versions prior to 8.2, see [Setting the python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

### Adding shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Server computer (by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offlinemode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
`pip download -r requirements.txt`. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the shell and click the shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Setting the python PythonOfflineRepositoryPath configuration key
Before PyPi Server was introduced as CloudShell’s python package management mechanism, the `PythonOfflineRepositoryPath` key was used to set the default offline package repository on the Quali Server machine, and could be used on specific Execution Server machines to set a different folder. 

**To set the offline python repository:**
1. Download the **[Shell Offline Requirements .zip File Name]** file, see [Downloading the Shell](#downloading-the-shell).

2. Unzip it to a local repository. Make sure the execution server has access to this folder. 

3.  On the Quali Server machine, in the *~\CloudShell\Server\customer.config* file, add the following key to specify the path to the default python package folder (for all Execution Servers):  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`

4. If you want to override the default folder for a specific Execution Server, on the Execution Server machine, in the *~TestShell\Execution Server\customer.config* file, add the following key:  
	`<add key="PythonOfflineRepositoryPath" value="repository 
full path"/>`

5. Restart the Execution Server.
 
### Configuring a new resource
This section explains how to create a new resource from the shell.

In CloudShell, the component that models the device is called a resource. It is based on the shell that models the device and allows the CloudShell user and API to remotely control the device from CloudShell.

You can also modify existing resources, see [Managing Resources in the Inventory](https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/create_a_resource_device.png).

**To create a resource for the device:**
  1. In the CloudShell Portal, in the **Inventory** dashboard, click **Add New**. 
     ![](https://github.com/stsuberi/SaraTest/blob/master/create_a_resource_device.png)
     
  2. From the list, select **[Shell Name]**.
  
  3. Enter the **Name** and **IP address** of the **[Device Name]** (if applicable).
  
  4. Click **Create**.
  
  5. In the **Resource** dialog box, enter the device's settings, see [Device Name Attributes](*device-name-attributes).
  
  6. Click **Continue**.

CloudShell validates the device’s settings and updates the new resource with the device’s structure (if the device has a structure).

# Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a shell that uses new/updated dependencies. It applies to both online and offline dependencies.

### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.

2. Extract the zip file to the suitable offline package folder(s).

3. Restart any execution server that has a live instance of the relevant driver or script. This requires running the Execution Server's configuration wizard, as explained in the [Configure the Execution Server](http://help.quali.com/doc/9.0/CS-Install/content/ig/configure%20cloudshell%20products/cfg-ts-exec-srver.htm?Highlight=configure%20the%20execution%20server) topic of the CloudShell Suite Installation guide. 

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, restart the execution server, as explained above. If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.

# Typical Workflow and Scenarios 
(edit as necessary depending on the shell)

**Scenario 1 - _Save configuration_** 
1. In CloudShell Portal, add the device resource to an active sandbox.

2. Run the **Save** command on the device with the following inputs:
    * **Folder Path**: For example, *tftp://ipaddress/shared folder* 
    * **Configuration Type**: **Running** or **Startup**

The configuration is saved to a file named *<ResourceName><startup/running-config>-<timestamp>*, which will reside in the folder path you entered.    

**Scenario 2 - _Restore Configuration_**
1. In CloudShell Portal, reserve the device resource.

2. Run the **Restore** resource command.

3. Enter the following parameters:
    * **Path** (mandatory): Enter the full path of the configuration file. 
    * **Restore Method** (optional): **Append** or **Override**. If you do not enter any value in this field, the **Append** method will be used. 
    * **Configuration Type** (mandatory): **Startup** or **Running**. 
	
**Scenario 3 - _Load firmware_**
1. In CloudShell Portal, reserve the device resource.

2. Run the **Load Firmware** resource command.

3. Enter the following parameters:
    * **Path** (mandatory): Enter the full path of the firmware file on the remote host. For example, *tftp://10.1.1.1/PanOS_200-5.0.5*. 
   
# References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation, see [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 

# Release Notes 
(if not applicable - remove section)
### What's New

* 
* 
* 

### Known Issues
* 
* 
* 
