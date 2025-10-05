package creationalPatterns

import "fmt"

// abstract factory 

type Shape interface {
	Draw()
}

type Circle struct {

}

func (c Circle) Draw() {
	fmt.Println("Circle!")
}

type Square struct {

}

func (s Square) Draw() {
	fmt.Println("Square!")
}

// factory method
func GetShape(shapeType string) Shape {
	switch shapeType {
		case "c": return Circle{}
		case "s": return Square{}
		default : return nil 
	}
}

// client code

func Factory() {
	c := GetShape("c")
	s := GetShape("s")
	c.Draw()
	s.Draw()
}
