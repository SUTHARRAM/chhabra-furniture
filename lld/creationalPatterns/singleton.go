// only single instance of a object is created with is globally accessible 
// logging 
// database obj etc. 

package creationalPatterns

import (
	"fmt"
	"sync"
)

type Logger struct {

}

var instance *Logger

var once sync.Once

func getLoggerObj() *Logger {
	once.Do(
		func() {
			instance = &Logger{}
		})

	return instance
}

func (l Logger) getLogMsg() {
	fmt.Println("This is message from logger!")
}

func SingleTon() {
	l1 := getLoggerObj()
	l2 := getLoggerObj()


	if l1 == l2 {
		fmt.Println("Both objects are similar")
	} else {
		fmt.Println("Both objects are not similar")
	}
}