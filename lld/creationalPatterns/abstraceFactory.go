package creationalPatterns

import "fmt"

// multple factories 

// abstrace product interface
type Button interface {
	Paint()
}
type CheckBox interface{
	Paint()
}

// Concrete Product Linux 

type LinuxButton struct {

}
type LinuxCheckBox struct {

}

func (b LinuxButton) Paint() {
	fmt.Println("Linux Button!")
}
func (b LinuxCheckBox) Paint() {
	fmt.Println("Linux CheckBox!")
}


// Mac Concrete Product
type MacButton struct {

}
type MacCheckBox struct {

}

func (b MacButton) Paint() {
	fmt.Println("Mac Button!")
}
func (b MacCheckBox) Paint() {
	fmt.Println("Mac CheckBox!")
}

// Abstrace Factory 

type GUIFactory interface {
	CreateButton() Button
	CreateChecBox() CheckBox
}

// Concrete Factories 
// mac
type MacFactory struct {

}

func (m MacFactory) CreateButton() Button{
	return MacButton{}
}

func (m MacFactory) CreateChecBox() CheckBox {
	return MacCheckBox{}
}

// linux
type LinuxFactory struct {

}

func (m LinuxFactory) CreateButton() Button{
	return LinuxButton{}
}

func (m LinuxFactory) CreateChecBox() CheckBox {
	return LinuxCheckBox{}
}

// render UI 

func renderUI(factory GUIFactory) {
	btn := factory.CreateButton()
	check := factory.CreateChecBox()

	btn.Paint()
	check.Paint()
}

// client 

func AbstraceFactory() {
	renderUI(MacFactory{})
	renderUI(LinuxFactory{})

}



