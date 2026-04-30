from . import(
    layer_comp,
    unity,
    preference,
    ui,
    menu,
)

module_list = (
    unity,
    layer_comp,
    preference,
    ui,
    menu,
)

def register():
    for mod in module_list:
        mod.register()

def unregister():
    for mod in reversed(module_list):
        mod.unregister()

if __name__ == "__main__":
    register()
