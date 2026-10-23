extends CharacterBody3D

enum State { IDLE, MOVE, AIR, LAND, CELEBRATE }

@export var speed := 5.0          # metres per second
@export var jump_velocity := 4.5  # metres per second, upward
@export var turn_speed := 10.0           # higher = snappier turning
@export var zoom_step := 1.0
@export var zoom_min := 2
@export var zoom_max := 10
@export var sprint_multiplier := 2.0
@export var land_anim_speed := 2.0

@export var mouse_sensitivity := 0.003
@onready var pivot: Node3D = $CameraPivot
@onready var arm: SpringArm3D = $CameraPivot/SpringArm3D
@onready var model: Node3D = $Model

@export var anim_blend := 0.2   # seconds of cross-fade between clips
@onready var anim: AnimationPlayer = $Model/Character/AnimationPlayer

var state := State.IDLE

func _ready() -> void:
	add_to_group("player")
	anim.animation_finished.connect(_on_animation_finished)

func _physics_process(delta: float) -> void:
	# Integrate acceleration into velocity: this one needs delta.
	if not is_on_floor():
		velocity += get_gravity() * delta

	var input := Input.get_vector("move_left", "move_right",
			"move_forward", "move_back")
	var direction := Vector3(input.x, 0, input.y).rotated(Vector3.UP, pivot.rotation.y)
	var sprinting := Input.is_action_pressed("sprint")

	match state:
		State.IDLE, State.MOVE:
			walk(direction, sprinting, delta)
			if Input.is_action_just_pressed("jump") and is_on_floor():
				velocity.y = jump_velocity
				change_state(State.AIR)
			elif not is_on_floor():
				change_state(State.AIR)              # walked off an edge
			elif direction.length() > 0.01:
				change_state(State.MOVE)
				anim.play("Sprint" if sprinting else "Walk", anim_blend)
			else:
				change_state(State.IDLE)
		State.AIR:
			walk(direction, sprinting, delta)        # air control
			if is_on_floor():
				change_state(State.LAND)
		State.LAND:
			if direction.length() > 0.01:
				change_state(State.MOVE)
			else:
				velocity.x = 0
				velocity.z = 0
		State.CELEBRATE:
			velocity.x = 0
			velocity.z = 0
		
	move_and_slide()

func change_state(new_state: State) -> void:
	if new_state == state:
		return                                   # enter actions run once, not every tick
	state = new_state
	match state:
		State.IDLE:
			anim.play("Idle", anim_blend)
		State.AIR:
			anim.play("Jump", anim_blend)
		State.LAND:
			anim.play("Jump_Land", 0.1, land_anim_speed)   # args: name, blend, speed	
		State.CELEBRATE:
			anim.play("Dance", anim_blend)

func walk(direction: Vector3, sprinting: bool, delta: float) -> void:
	var current_speed := speed * (sprint_multiplier if sprinting else 1.0)
	velocity.x = direction.x * current_speed
	velocity.z = direction.z * current_speed
	if direction.length() > 0.01:
		var target_yaw := atan2(-direction.x, -direction.z)
		model.rotation.y = lerp_angle(model.rotation.y, target_yaw, turn_speed * delta)

func _on_animation_finished(anim_name: StringName) -> void:
	if state == State.LAND:
		change_state(State.IDLE)

func celebrate() -> void:
	change_state(State.CELEBRATE)

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
