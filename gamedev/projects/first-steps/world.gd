extends Node3D

@onready var score_label: Label = $HUD/scorelabel   # looked up once _ready runs

var score := 0
var total := 0
signal collected_all 

func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	
	var coins := $coins.get_children()   # coins are already ready (children first)
	total = coins.size()
	for coin in coins:
		coin.collected.connect(_on_coin_collected)
	update_label()

	collected_all.connect($player.celebrate)

func _on_coin_collected() -> void:
	score += 1
	update_label()

func update_label() -> void:
	if score == total:
		score_label.text = "You found all the coins!"
		collected_all.emit()
	else:
		score_label.text = "Coins: %d / %d" % [score, total]
