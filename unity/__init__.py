from . import(
    preset,
    mask,
    effect,
    layer,
    compositor,
    output,
)

module_list = (
    preset,
    mask,
    effect,
    layer,
    compositor,
    output,
)

def register():
    for mod in module_list:
        mod.register()
        
def unregister():
    for mod in reversed(module_list):
        mod.unregister()

if __name__ == "__main__":
    register()
