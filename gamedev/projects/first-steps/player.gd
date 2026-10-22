extends CharacterBody3D

@export var speed := 5.0          # metres per second
@export var jump_velocity := 4.5  # metres per second, upward
@export var turn_speed := 10.0           # higher = snappier turning

@export var mouse_sensitivity := 0.003
@onready var pivot: Node3D = $CameraPivot
@onready var arm: SpringArm3D = $CameraPivot/SpringArm3D
@onready var model: Node3D = $Model

func _ready() -> void:
	add_to_group("player")

func _physics_process(delta: float) -> void:
	# Integrate acceleration into velocity: this one needs delta.
	if not is_on_floor():
		velocity += get_gravity() * delta

	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity

	var input := Input.get_vector("move_left", "move_right",
			"move_forward", "move_back")
	var direction := Vector3(input.x, 0, input.y).rotated(Vector3.UP, pivot.rotation.y)

	velocity.x = direction.x * speed
	velocity.z = direction.z * speed

	if direction.length() > 0.01:
		var target_yaw := atan2(-direction.x, -direction.z)
		model.rotation.y = lerp_angle(model.rotation.y, target_yaw, turn_speed * delta)

	# Velocity into position, with collisions. Delta applied inside.
	move_and_slide()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		pivot.rotation.y -= event.relative.x * mouse_sensitivity
		arm.rotation.x -= event.relative.y * mouse_sensitivity
		arm.rotation.x = clampf(arm.rotation.x, deg_to_rad(-70.0), deg_to_rad(20.0))
	elif event.is_action_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	elif event is InputEventMouseButton and event.pressed:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
