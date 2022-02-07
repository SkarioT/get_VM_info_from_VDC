
import atexit
 
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
import subprocess as sp
import getpass
 

USER = input("Username:")
PSWD = getpass.getpass("Pasword:")



SERVER1="exemple1.vsphere-server.com"
SERVER2="exemple2.vsphere-server.com"
 
TEST_VM_NAME="mng-vLbp"

file_name="output"


 
def main():

    def Connecotr_no_vspher(server):
        resault_str=""
        
        try:
            service_instance = connect.SmartConnect(host=server,
                                                    user=USER,
                                                    # pwd=PSWD[::-1],
                                                    pwd=PSWD,
                                                    port=443,disableSslCertValidation=True)
    
            atexit.register(connect.Disconnect, service_instance)
    
            content = service_instance.RetrieveContent()
    
            container = content.rootFolder  # starting point to look into
            viewType = [vim.VirtualMachine]  # object types to look for
            recursive = True  # whether we should look into it recursively
            containerView = content.viewManager.CreateContainerView(
                container, viewType, recursive)
    
            children = containerView.view

            i=1
            
            #цикл вывода информации по имени вм и к какому ресурсному пулу (vdc) она относится
            for child in children:
                vm_name=child.summary.config.name
                try:
                    #получаю VDC, из полученного VDC вытаскию только УНП
                    vm_vdc_name=(child.resourcePool.name).split("_")[0].split(" ")[0]
                    #вывожу на печаль сопоставлене ВМ <-> УНП
                    # print(f"{i}_VM_name: {vm_name}".ljust(80),f" Resoure_poll: {vm_vdc_name}".ljust(50)) #get resourse poll for vm
                    resault_str+=f"{vm_vdc_name}".ljust(20) +"  "+vm_name+"\n"

                except:
                    pass
                    # print(f"{i}_VM_name: {vm_name}".ljust(80))
                i+=1
        except vmodl.MethodFault as error:
            print("Caught vmodl fault : " + error.msg)
            
            
        
        return resault_str.encode("ascii",'ignore').decode("ascii",'ignore')
#_________________________________________________________________________________________________
    resault_str1=Connecotr_no_vspher(SERVER1)
    if len(resault_str1) == 0:
        input("\nPress any key for closed")
        return
    resault_str2=Connecotr_no_vspher(SERVER2)
    resault_str=resault_str1+resault_str2

    file_all_VMs_txt="all_VMs.txt"
    with open(file_all_VMs_txt,'w') as fp:
        fp.write(resault_str)

    # открыуваю на чтение файлы 
    f_all = open('all_VMs.txt', 'r')
    try:
        f_find = open('input.txt', 'r')
    except:
        print("\n\n\nDon't find input.txt !!!\nOnly create \"all_VMs.txt\"\n\n")
        return 

        #заношу в перменные содержимое файлов в качестве листа
    list_all_vms=f_all.readlines()
    list_find_vms=f_find.readlines()
    len_list_all_vms=len(list_all_vms)
    len_list_find_vms=len(list_find_vms)

    
    i=0
    j=0
    ok=0
    res_out=""
    res_unp=""
    for find_vm_num in range(len_list_find_vms):
        for i in range(len_list_all_vms):
            if list_find_vms[find_vm_num].split("\n")[0]  in list_all_vms[i]:
                #если имя ВМ  начинаетс с VSE
                if list_find_vms[find_vm_num].startswith("vse"):
                    #разбиваю имя, получаю 2 слово равное УНП
                    unp_from_name= list_find_vms[find_vm_num].split("-")[1].split("_")[0]
                    #заменяю системное имя EDGE ( System) на полученное из имени УНП
                    
                    list_all_vms[i]=list_all_vms[i].replace("System",unp_from_name)#.replace("   ","")
                    
                res_out+=list_all_vms[i]
                res_unp+=list_all_vms[i].split("  ")[0]+"\n"
                break
            elif (i+1)==len_list_all_vms :
                res_out+="\nNOT_FOUND"+"  "+list_find_vms[find_vm_num].split("\n")[0]+"\n\n"
                
    file_res="output.txt"
    with open(file_res,'w') as fp:
        fp.write(res_out)
        programName = "notepad.exe"
        sp.Popen([programName, file_res])
    file_unp="unp_all.txt"
    with open(file_unp,'w') as fp:
        fp.write(res_unp)
        programName = "notepad.exe"
        sp.Popen([programName, file_unp])
    uniqlines = set(open(file_unp, 'r').readlines())
    gotovo = open('unp.txt','w').writelines(set(uniqlines))
    programName = "notepad.exe"
    sp.Popen([programName, 'unp.txt'])
                    
 
# Start program
if __name__ == "__main__":
    main()

