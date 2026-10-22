extends MeshInstance3D

@export var spin_speed := 1.5   # radians per second
@export var move_speed := 3.0   # metres per second

func _process(delta: float) -> void:
	rotate_y(spin_speed * delta)
	var input := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	position += Vector3(input.x, 0, input.y) * move_speed * delta
