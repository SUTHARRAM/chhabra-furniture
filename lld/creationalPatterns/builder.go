// when objects requres to many configration and too many params have in constructure.

package creationalPatterns

import "fmt"

type Computer struct {
	GPU, CPU, RAM string
}

type ComputerBuilder struct {
	computer Computer
}

func (b *ComputerBuilder) setRam(ram string) *ComputerBuilder {
	b.computer.RAM = ram
	return b
}

func (b *ComputerBuilder) setGpu(gpu string) *ComputerBuilder {
	b.computer.GPU = gpu
	return b
}

func (b *ComputerBuilder) setCpu(cpu string) *ComputerBuilder {
	b.computer.CPU = cpu
	return b
}

func (b *ComputerBuilder) Build() Computer {
	return b.computer
}

func NewComputerBuilder() *ComputerBuilder {
	cp := ComputerBuilder{}
	return &cp
}

func Builder() {
	newComputer := NewComputerBuilder().
					setRam("TestRam").
					setGpu("TestGPU").
					setCpu("TestCPU").
					Build()

	fmt.Println("This is my PC", newComputer)


}