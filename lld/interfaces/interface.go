package main

import ("fmt")

type ATM interface {
	Withdraw(float64) bool
	Desposit(float64) bool
}

type AtmMachine struct {
	atm ATM
}


type AtmCard struct{
	des string 
}

func (a AtmCard) Withdraw(amount float64) bool {
	fmt.Println("collect cash : ", amount)
	return true
} 

func (a AtmCard) Desposit(amount float64) bool {
	fmt.Println("Desosited cash : ", amount) 
	return true
}

/////////////////// 

// metro card 

type MetroCard struct {
	des string
}

func (m MetroCard) Withdraw(amount float64) bool {
	fmt.Println("collet cash through metro card : ", amount)

	return true
}

func (m MetroCard) Desposit(amount float64) bool {
	fmt.Println("desposited cash through metro card : ", amount)

	return true
}



func main() {

	// atm withdral 

	rupeeCard := AtmCard{des: "This is ATM Card"}

	atmMachine := AtmMachine{atm: rupeeCard}


	fmt.Println("atm withdraw : ", atmMachine.atm.Withdraw(1000.00), " deposit atm : ", atmMachine.atm.Desposit(55.34))

	metroCard := MetroCard{des: "This is ATM Card"}

	atmMachine = AtmMachine{atm: metroCard}


	fmt.Println("atm withdraw : ", atmMachine.atm.Withdraw(1000.00), " deposit atm : ", atmMachine.atm.Desposit(55.34))
}