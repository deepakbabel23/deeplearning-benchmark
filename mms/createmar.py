from zipfile import ZipFile
import os
import sys
import shutil
import json

def create_manifest(model,name_suffix, version):
    mar = {
              "runtime": "python",
              "model": {
                "modelName": "resnet-18",
                "serializedFile": "resnet18-5c106cde.pth",
                "handler": "image_classifier",
                "modelFile": "model.py",
                "modelVersion": "1.0"
              },
              "modelServerVersion": "1.0",
              "implementationVersion": "1.0",
              "specificationVersion": "1.0"
            }

    mar["model"]["modelVersion"] = version
    mar["model"]["modelName"] = mar["model"]["modelName"]+'_'+name_suffix

    with open(model+"/MAR-INF/MANIFEST.json", "w") as data_file:
        json.dump(mar, data_file, indent=2)

def create_mar( ):
    for i in range(1,mar_count+1):
        model = model_dir+'_'+str(i)
        if os.path.isdir(model):
            shutil.rmtree(model)
        shutil.copytree(model_dir, model)
        create_manifest(model,str(i), str(float(i)))
        mar = model+'.mar'
        if os.path.exists(mar):
            os.remove(mar)
        with ZipFile(mar, 'w') as zipObj:
           # Iterate over all the files in directory
           for folderName, subfolders, filenames in os.walk(model):
               for filename in filenames:
                   zipObj.write(os.path.join(folderName, filename), arcname=os.path.join(folderName.replace(model, ""), filename))

        shutil.rmtree(model)
        print("Completed MAR: "+mar)

#model_dir = sys.argv[1]
#mar_count = sys.argv[2]

model_name = 'resnet-18'
base_dir = '/home/ubuntu/model_store'
#base_dir = '/Users/dhaniram_kshirsagar/projects/neo-sagemaker/mms/testing/model_store'
mar_count = 100
model_dir = base_dir + '/' +model_name

create_mar()
