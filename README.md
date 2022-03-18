### Features

**get_VMs_vdc_names** - a script which allows you to get information from vSphere containing information in the form of a pair of values:

**VM_NAMES <-> TIN_NAMES**

Installation:
`$ pip install -r requirements.txt`

This script is primarily designed to speed up handling an incident, for example, a host restart.
We get the list of affected VMs. Throw them into file** input.txt**


The script will result in 1 or 4 output files:

-**all_VMs.txt** - file containing all VMs from two vSphere hosts in mapped form: TIN Name_VM. File is created under any condition.

-**output.txt** - file containing search result, by VM names, based on VM names in input.txt file. Input.txt file must be located in the same directory as the script.

-**unp_all.txt**- file containing all TINs obtained from names of VMs located in **input.txt** Contains duplicates as >=1 VMs can belong to the same organization.

-**unp.txt** - file containing all TINs received from VMs located in **input.txt** file. Does not contain duplicates, file is suitable for work of **Wiki3** script at once
