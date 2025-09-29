package linkedlist

import "fmt"

type Node struct {
	Val  interface{}
	Next *Node
}

type Linkedlist struct {
	Head *Node
	Count int
}

func (l *Linkedlist) AddNode(val interface{}) {
	newNode := &Node{Val: val, Next: nil}

	if l.Head == nil {
		l.Head = newNode
		l.Count++
	} else {
		node := l.Head
		for node.Next != nil {
			node = node.Next
			
		}
		node.Next = newNode
		l.Count++
	}
}

func (l *Linkedlist) PrintLinkedList() {
	if l.Head == nil {
		fmt.Println("Linked List Is Empty!")
		return
	} 

	fmt.Println("LinkedList Size : ", l.Count)

	fmt.Println("Here is the complete linkedlist :- ")

	node := l.Head

	for node.Next != nil {
		fmt.Print(node.Val, "->")
		node = node.Next
	}

	fmt.Print(node.Val)

	fmt.Println("")
}

func (l *Linkedlist) SearchElement(val interface{}) {
	if l.Head == nil {
		fmt.Println("Linked LIst is empty")
		return 
	}

	if l.Head.Val == val {
		fmt.Println("Element found ", l.Head.Val)
		return
	}

	tempNode := l.Head
	for tempNode.Next != nil {
		if tempNode.Val == val {
			fmt.Println("Element found ", tempNode.Val)
			return
		}
		tempNode = tempNode.Next
	}

	if tempNode.Val == val {
		fmt.Println("Element found ", tempNode.Val)
		return
	}

	fmt.Println("Element Not Present!")
}

func (l *Linkedlist) UpdateNode(val interface{}, newVal interface{}) {
	if l.Head == nil {
		fmt.Println("LinkedList Is Empty")
		return
	}

	if l.Head.Val == val {
		l.Head.Val = newVal
		fmt.Println("Value Updated")
		return
	}

	temp := l.Head

	for temp.Next != nil {
		if temp.Val == val {
			temp.Val = newVal
			fmt.Println("Value Updated")
			return
		}
		temp = temp.Next

	}

	if temp.Val == val {
		temp.Val = newVal
		fmt.Println("Value Updated")
		return
	}

	fmt.Println("Value Not Found")

}


func LinkedListImplementation() {
	var linkedl  Linkedlist

	linkedl.AddNode(5)
	linkedl.AddNode(6)
	linkedl.AddNode(7)
	linkedl.AddNode(8)
	linkedl.AddNode(9)
	linkedl.AddNode(10)
	linkedl.AddNode(11)
	linkedl.AddNode(12)
	linkedl.AddNode("abc")
	linkedl.AddNode("Ram")
	linkedl.AddNode(12.43)

	linkedl.PrintLinkedList()

	linkedl.SearchElement(11)

	linkedl.SearchElement("Ram")

	linkedl.SearchElement("Chhabra")

	fmt.Println("Node Updation :- ")

	linkedl.UpdateNode(5, "My")
	linkedl.UpdateNode(6, "Name")
	linkedl.UpdateNode(7, "is")
	linkedl.UpdateNode(8, "Ram")
	linkedl.UpdateNode(9, "Chhabra")
	linkedl.UpdateNode(10, 300)
	linkedl.UpdateNode("This", 5)

	linkedl.PrintLinkedList()


}
