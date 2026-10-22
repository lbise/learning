extends Area3D

signal collected   # custom signal: "I was picked up"

func _ready() -> void:
	body_entered.connect(_on_body_entered)   # built-in signal → my handler

func _process(delta: float) -> void:
	rotate_y(3.0 * delta)                    # purely visual spin

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		collected.emit()
		queue_free()                         # delete me at the end of this frame
