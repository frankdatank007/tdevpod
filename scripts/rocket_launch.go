// rocket_launch.go: countdown for a cardboard rocket (display-only theatre)
package main

import (
	"fmt"
	"strings"
	"time"
)

type Rocket struct {
	Name     string
	Fuel     int
	Stickers []string
}

func (r *Rocket) Refuel(amount int) {
	r.Fuel += amount
	if r.Fuel > 100 {
		r.Fuel = 100
	}
}

func bar(pct int) string {
	filled := pct / 5
	return "[" + strings.Repeat("█", filled) + strings.Repeat("░", 20-filled) + "]"
}

func main() {
	r := &Rocket{Name: "Cardboard-1", Stickers: []string{"star", "moon", "dino"}}
	for r.Fuel < 100 {
		r.Refuel(5)
		fmt.Printf("\r%s %3d%%  fueling %s", bar(r.Fuel), r.Fuel, r.Name)
		time.Sleep(120 * time.Millisecond)
	}
	fmt.Println("\n3... 2... 1... blast off to the kitchen!")
}

// $ go run rocket_launch.go
[░░░░░░░░░░░░░░░░░░░░]   0%  fueling Cardboard-1
[█░░░░░░░░░░░░░░░░░░░]   5%  fueling Cardboard-1
[██░░░░░░░░░░░░░░░░░░]  10%  fueling Cardboard-1
[███░░░░░░░░░░░░░░░░░]  15%  fueling Cardboard-1
[████░░░░░░░░░░░░░░░░]  20%  fueling Cardboard-1
[█████░░░░░░░░░░░░░░░]  25%  fueling Cardboard-1
[██████░░░░░░░░░░░░░░]  30%  fueling Cardboard-1
[███████░░░░░░░░░░░░░]  35%  fueling Cardboard-1
[████████░░░░░░░░░░░░]  40%  fueling Cardboard-1
[█████████░░░░░░░░░░░]  45%  fueling Cardboard-1
[██████████░░░░░░░░░░]  50%  fueling Cardboard-1
[███████████░░░░░░░░░]  55%  fueling Cardboard-1
[████████████░░░░░░░░]  60%  fueling Cardboard-1
[█████████████░░░░░░░]  65%  fueling Cardboard-1
[██████████████░░░░░░]  70%  fueling Cardboard-1
[███████████████░░░░░]  75%  fueling Cardboard-1
[████████████████░░░░]  80%  fueling Cardboard-1
[█████████████████░░░]  85%  fueling Cardboard-1
[██████████████████░░]  90%  fueling Cardboard-1
[███████████████████░]  95%  fueling Cardboard-1
[████████████████████] 100%  fueling Cardboard-1
3... 2... 1... blast off to the kitchen!
