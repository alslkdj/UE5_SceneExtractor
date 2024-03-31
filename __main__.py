import unreal
import json


class jsonStruct:
    resource_name = ''
    
    location = []
    rotation = []
    scale = []

    def __init__ (self, resource_name, location, rotation, scale):
        self.resource_name = resource_name

        self.location = location
        self.rotation = rotation
        self.scale = scale
    
    def show (self):
        jsonDic = {
            "ResourceName": self.resource_name,

            "Location": self.location,
            "Rotation": self.rotation,
            "Scale": self.scale

        }
        return(jsonDic)

#인자로 받은 액터의 정보 추출해서 반환        
def ExtractStaticMeshData(actor):
    SM_Component = actor.get_component_by_class(unreal.StaticMeshComponent)
    staticMesh = SM_Component.static_mesh

    if staticMesh is not None:
        location = [actor.get_actor_location().x, actor.get_actor_location().y, actor.get_actor_location().z]
        #rotation = [actor.get_actor_rotation().roll, actor.get_actor_rotation().pitch, actor.get_actor_rotation().yaw]
        rotation = [actor.get_actor_rotation().quaternion().w, actor.get_actor_rotation().quaternion().x, actor.get_actor_rotation().quaternion().y, actor.get_actor_rotation().quaternion().z]
        scale = [actor.get_actor_scale3d().x, actor.get_actor_scale3d().y, actor.get_actor_scale3d().z]

        testStruct = jsonStruct(staticMesh.get_name(), location, rotation, scale)

        return testStruct.show()
    
    else: return None

def ExtractFoliageData(actor:unreal.InstancedFoliageActor):
    tempArr = []
    instanced_SM_Component = actor.get_components_by_class(unreal.InstancedStaticMeshComponent)
    for inst_staticMesh in instanced_SM_Component:
        if inst_staticMesh is not None:
            count = inst_staticMesh.get_instance_count()
            for i in range(0, count):
                transform = inst_staticMesh.get_instance_transform(i, True)
                location = [transform.translation.x, transform.translation.y, transform.translation.z]
                rotation = [transform.rotation.w, transform.rotation.x, transform.rotation.y, transform.rotation.z]
                scale = [transform.scale3d.x, transform.scale3d.y, transform.scale3d.z]

                testStruct = jsonStruct(inst_staticMesh.static_mesh.get_name(), location, rotation, scale)
                tempArr.append(testStruct.show())
    if tempArr is not None : return tempArr
    else: return None




#현재 에디터상 월드 참조
unrealEditorSubSystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
currentWorld = unrealEditorSubSystem.get_editor_world()


#현재 월드의 모든 스태틱메시액터 긁어옴
SM_ActorArr = unreal.GameplayStatics.get_all_actors_of_class(currentWorld, unreal.StaticMeshActor)

#현재 월드의 모든 폴리지액터 긁어옴
Foliage_ActorArr = unreal.GameplayStatics.get_all_actors_of_class(currentWorld, unreal.InstancedFoliageActor)

#json 오브젝트들을 저장할 배열
json_Arr = []

#긁은 액터 추출돌리기
for actor in SM_ActorArr:
    extractData = ExtractStaticMeshData(actor)
    if extractData is not None:
        json_Arr.append(extractData)

for actor in Foliage_ActorArr:
    extractData = ExtractFoliageData(actor)
    if extractData is not None:
        json_Arr.extend(extractData)

#언리얼 Execute Python Script 노드에서 인자를 받아서 주소 완성
fileDir = dir + file_name + '.json'

#json 파일에 저장
with open(fileDir, 'w') as f:
    json.dump(json_Arr, f, indent=2)
