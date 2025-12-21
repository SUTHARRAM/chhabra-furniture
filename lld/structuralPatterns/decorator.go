package structuralPatterns

import (
	"fmt"
)

type Coffee interface {
	Cost() int 
	Description() string
}


type SimpleCofee struct {
}

func (c SimpleCofee) Cost() int {

	return 5
}

func (c SimpleCofee) Test() int {

	return 5
}

func (d SimpleCofee) Description() string {
	return "This is Simple Coffee! "
}

type CoffeeDecorator struct {
	coffee Coffee
}

type SuggerCoffee struct {
	CoffeeDecorator
}

func (s SuggerCoffee) Cost() int {
	return s.coffee.Cost() + 5
}

func (s SuggerCoffee) Description() string {
	return s.coffee.Description() + " With Sugger!"
}



func Decorator() {
	var myCoffee Coffee = SimpleCofee{}

	fmt.Println("Coffee => ", myCoffee.Description(), " Price => ", myCoffee.Cost())

//	fmt.Printf("Type of my Coffee %T ", myCoffee)

	myCoffee = SuggerCoffee{CoffeeDecorator{coffee : myCoffee}}

	fmt.Println("Coffee => ", myCoffee.Description(), " Price => ", myCoffee.Cost())


}