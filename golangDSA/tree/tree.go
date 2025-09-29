package tree

import "fmt"

type Node struct {
	val   int
	left  *Node
	right *Node
}


func (t *Node) Insert(val int) {
	
	if t.val > val {
		if t.left == nil {
			t.left = &Node{val:val}
		} else {
			t.left.Insert(val)
		}
	} else {
		if t.right == nil {
			t.right = &Node{val:val}
		} else {
			t.right.Insert(val)
		}
	}
}

func (t *Node) PreOrder() {
	if t == nil {
		return
	}
	fmt.Print(t.val, ", ")
	t.left.PreOrder()
	t.right.PreOrder()
}

func Tree() {
	var root = Node{val:20}

	root.Insert(12)
	root.Insert(30)
	root.Insert(8)
	root.Insert(15)
	root.Insert(5)
	root.Insert(10)
	root.Insert(13)
	root.Insert(16)
	root.Insert(25)
	root.Insert(35)

	root.PreOrder()


}
