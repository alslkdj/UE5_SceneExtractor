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
def ExtractMeshData(actor):
    SM_Component = actor.get_component_by_class(unreal.StaticMeshComponent)
    staticMesh = SM_Component.static_mesh

    location = [actor.get_actor_location().x, actor.get_actor_location().y, actor.get_actor_location().z]
    #rotation = [actor.get_actor_rotation().roll, actor.get_actor_rotation().pitch, actor.get_actor_rotation().yaw]
    rotation = [actor.get_actor_rotation().quaternion().w, actor.get_actor_rotation().quaternion().x, actor.get_actor_rotation().quaternion().y, actor.get_actor_rotation().quaternion().z]
    scale = [actor.get_actor_scale3d().x, actor.get_actor_scale3d().y, actor.get_actor_scale3d().z]

    testStruct = jsonStruct(staticMesh.get_name(), location, rotation, scale)

    return testStruct.show()

#현재 에디터상 월드 참조
currentWorld = unreal.EditorLevelLibrary.get_editor_world()

#현재 월드의 모든 스태틱메시액터 긁어옴
SM_ActorArr = unreal.GameplayStatics.get_all_actors_of_class(world_context_object=currentWorld, actor_class=unreal.StaticMeshActor)

#json 오브젝트들을 저장할 배열
json_Arr = []

#긁은 액터 추출돌리기
for actor in SM_ActorArr:
    json_Arr.append(ExtractMeshData(actor))

#언리얼 Execute Python Script 노드에서 인자를 받아서 주소 완성
fileDir = dir + file_name + '.json'

#json 파일에 저장
with open(fileDir, 'w') as f:
    json.dump(json_Arr, f, indent=2)
