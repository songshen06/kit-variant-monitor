import omni.ext
import omni.ui as ui
import omni.usd
import omni.kit.viewport.utility
from pxr import Usd, Tf

class MyViewportButtonsExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[MyViewportButtons] MyViewportButtonsExtension startup")

        self._window_example = None
        self._tracked_prims = []  # Initialize list to track multiple prims
        self._dialog = None
        self._path_model = None
        self._button_container = None  # Initialize button container
        self._update_subscription = None
        self._resizing = False
        self._resize_start_pos = None
        self._initial_size = None
        self._dragging = False
        self._drag_start_pos = None
        self._initial_pos = None

        self._build_ui()

    def _build_ui(self):
        # Create a dialog to select the tracked prim
        self._create_dialog()

        # Create and show the button window
        self.create_and_show_window()

    def _create_dialog(self):
        self._dialog = ui.Window("Select Prims", width=300, height=150)
        with self._dialog.frame:
            with ui.VStack():
                ui.Label("Enter Prim Paths (comma-separated):")
                self._path_model = ui.SimpleStringModel()
                ui.StringField(model=self._path_model)
                ui.Button("Track Prims", clicked_fn=self._on_track_prims)

    def create_and_show_window(self):
        if not self._window_example:
            self._window_example = ui.Window("Prim Variants", width=300, height=400)

            with self._window_example.frame:
                with ui.VStack():
                    self._drag_bar = ui.Rectangle(height=20, style={"background_color": 0xff888888}, mouse_pressed_fn=self._on_drag_start, mouse_released_fn=self._on_drag_end, mouse_moved_fn=self._on_drag_move)
                    ui.Spacer(height=10)  # Add space to push the buttons down
                    self._button_container = ui.ScrollingFrame(height=300)  # Use ScrollingFrame for the buttons
                    with self._button_container:
                        self._button_vstack = ui.VStack()

        self._window_example.visible = True

    def _on_track_prims(self):
        prim_paths = self._path_model.get_value_as_string().split(',')
        stage = omni.usd.get_context().get_stage()
        self._tracked_prims = [stage.GetPrimAtPath(prim_path.strip()) for prim_path in prim_paths if stage.GetPrimAtPath(prim_path.strip()).IsValid()]

        if self._tracked_prims:
            print(f"Tracking Prims: {[prim.GetPath() for prim in self._tracked_prims]}")
            self._update_buttons()
            self._subscribe_to_changes()
        else:
            print("No valid Prim Paths")

    def _update_buttons(self):
        if self._tracked_prims:
            # Clear existing buttons
            self._button_vstack.clear()

            for prim in self._tracked_prims:
                prim_label = ui.Label(f"Prim: {prim.GetPath()}", height=20)  # Add label for each prim
                variant_sets = prim.GetVariantSets()
                with self._button_vstack:
                    for variant_set_name in variant_sets.GetNames():
                        variant_set = variant_sets.GetVariantSet(variant_set_name)
                        for variant_name in variant_set.GetVariantNames():
                            print(f"Adding button for variant: {variant_set_name}: {variant_name}")  # Debug information
                            ui.Button(f"{variant_set_name}: {variant_name}", width=150, height=30, clicked_fn=lambda vs=variant_set_name, vn=variant_name, p=prim: self._on_button_click(p, vs, vn))

    def _on_button_click(self, prim, variant_set_name, variant_name):
        print(f"Button {variant_set_name}: {variant_name} clicked for prim {prim.GetPath()}")
        variant_sets = prim.GetVariantSets()
        variant_set = variant_sets.GetVariantSet(variant_set_name)
        variant_set.SetVariantSelection(variant_name)
        print(f"Set {variant_set_name} to {variant_name} for prim {prim.GetPath()}")

    def _subscribe_to_changes(self):
        if self._update_subscription:
            self._update_subscription.Revoke()  # Unsubscribe from previous subscription

        # Subscribe to USD changes
        self._update_subscription = Tf.Notice.Register(Usd.Notice.ObjectsChanged, self._on_usd_change, omni.usd.get_context().get_stage())
        print(f"Subscribed to USD changes for stage: {omni.usd.get_context().get_stage().GetRootLayer().identifier}")

    def _on_usd_change(self, notice, stage):
        changed_paths = notice.GetChangedInfoOnlyPaths()
        for path in changed_paths:
            print(f"USD change detected at path: {path}")  # Debug information
            for prim in self._tracked_prims:
                if path.GetPrimPath() == prim.GetPath():
                    print(f"Detected change in prim: {path}")
                    self._update_buttons()
                    return

    def _on_drag_start(self, x, y, button, modifiers):
        self._dragging = True
        self._drag_start_pos = (x, y)
        self._initial_pos = (self._window_example.x, self._window_example.y)

    def _on_drag_end(self, x, y, button, modifiers):
        self._dragging = False

    def _on_drag_move(self, x, y, dx, dy):
        if self._dragging:
            new_x = self._initial_pos[0] + (x - self._drag_start_pos[0])
            new_y = self._initial_pos[1] + (y - self._drag_start_pos[1])
            self._window_example.set_position(new_x, new_y)

    def _on_resize_start(self, x, y, button, modifiers):
        self._resizing = True
        self._resize_start_pos = (x, y)
        self._initial_size = (self._window_example.width, self._window_example.height)

    def _on_resize_end(self, x, y, button, modifiers):
        self._resizing = False

    def _on_resize_move(self, x, y, dx, dy):
        if self._resizing:
            new_width = max(self._initial_size[0] + dx, 200)  # Minimum width
            new_height = max(self._initial_size[1] + dy, 200)  # Minimum height
            self._window_example.width = new_width
            self._window_example.height = new_height
            self._button_container.height = new_height - 100  # Adjust scrolling frame height

    def on_shutdown(self):
        print("[MyViewportButtons] MyViewportButtonsExtension shutdown")
        self._dialog = None
        self._window_example = None
        self._button_vstack = None
        if self._update_subscription:
            self._update_subscription.Revoke()
            self._update_subscription = None

def get_active_viewport_window():
    viewport_window = omni.kit.viewport.utility.get_active_viewport_window()
    if viewport_window:
        return viewport_window
    else:
        raise RuntimeError("Failed to get active viewport window")
