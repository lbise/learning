extends CharacterBody3D

@export var speed := 5.0          # metres per second
@export var jump_velocity := 4.5  # metres per second, upward
@export var turn_speed := 10.0           # higher = snappier turning
@export var zoom_step := 1.0
@export var zoom_min := 2
@export var zoom_max := 10
@export var sprint_mod := 2.0

@export var mouse_sensitivity := 0.003
@onready var pivot: Node3D = $CameraPivot
@onready var arm: SpringArm3D = $CameraPivot/SpringArm3D
@onready var model: Node3D = $Model

@export var anim_blend := 0.2   # seconds of cross-fade between clips
@onready var anim: AnimationPlayer = $Model/Character/AnimationPlayer

func _ready() -> void:
	add_to_group("player")

var celebrating := false
func celebrate() -> void:
	celebrating = true
	anim.play("Dance", anim_blend)

func _physics_process(delta: float) -> void:
	if celebrating:
		velocity.x = 0
		velocity.z = 0
		move_and_slide()
		return

	# Integrate acceleration into velocity: this one needs delta.
	if not is_on_floor():
		velocity += get_gravity() * delta

	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity

	var input := Input.get_vector("move_left", "move_right",
			"move_forward", "move_back")
	var direction := Vector3(input.x, 0, input.y).rotated(Vector3.UP, pivot.rotation.y)

	var mod = 1
	var sprinting := Input.is_action_pressed("sprint")
	if sprinting:
		mod = sprint_mod

	velocity.x = direction.x * speed * mod
	velocity.z = direction.z * speed * mod

	if direction.length() > 0.01:
		var target_yaw := atan2(-direction.x, -direction.z)
		model.rotation.y = lerp_angle(model.rotation.y, target_yaw, turn_speed * delta)

	# Velocity into position, with collisions. Delta applied inside.
	move_and_slide()
	update_animation(direction, sprinting)

func update_animation(direction: Vector3, sprinting: bool) -> void:
	if not is_on_floor():
		anim.play("Jump", anim_blend)
	elif direction.length() > 0.01:
		# TODO 2: "Sprint" while sprinting, otherwise "Walk"
		if sprinting:
			anim.play("Sprint", anim_blend)
		else:
			anim.play("Walk", anim_blend)
	else:
		anim.play("Idle", anim_blend)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		pivot.rotation.y -= event.relative.x * mouse_sensitivity
		arm.rotation.x -= event.relative.y * mouse_sensitivity
		arm.rotation.x = clampf(arm.rotation.x, deg_to_rad(-70.0), deg_to_rad(20.0))
	elif event.is_action_pressed("ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	elif event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			arm.spring_length -= zoom_step
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			arm.spring_length += zoom_step
		else:
			Input.mouse_mode = Input.MOUSE_MODE_CAPTURED   # real clicks still recapture
			
		arm.spring_length = clampf(arm.spring_length, zoom_min, zoom_max)
