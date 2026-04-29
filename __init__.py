from . import(
    layer_comp,
    unity,
    preference,
    ui,
)

module_list = (
    unity,
    layer_comp,
    preference,
    ui,
)

def register():
    for mod in module_list:
        mod.register()

def unregister():
    for mod in reversed(module_list):
        mod.unregister()

if __name__ == "__main__":
    register()
