package queue

import "fmt"

/*
- Enqueue
- Dequeue
- Size
- IsEmpty

*/

type Queue struct {
	items []interface{}
}

func (q *Queue) Enqueue(val interface{}) {
	q.items = append(q.items, val)
}

func (q *Queue) Dequeue() {
	if q.IsEmpty().(bool) {
		fmt.Println("Queue Is Empty!")
	}

	fmt.Println("Item Dequeued : ", q.items[0])

	q.items = q.items[1:]
}

func (q *Queue) Size() interface{} {
	return len(q.items)
}

func (q *Queue) IsEmpty() interface{} {
	return len(q.items) == 0
}

func (q *Queue) Print() {
	if q.IsEmpty().(bool) {
		fmt.Println("Queue Is Empty")
	}

	for _, item := range q.items {
		fmt.Print(item, ", ")
	}
}

func QueueImplementation() {
	var q Queue

	q.Enqueue(334)
	q.Enqueue("gsg")
	q.Enqueue(4324.34)
	q.Enqueue(true)
	q.Enqueue(false)
	q.Enqueue(0.322)

	q.Print()

	q.Size()

	q.Dequeue()

	q.Size()

	q.Print()


}

