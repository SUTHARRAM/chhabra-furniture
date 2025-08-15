package util

import (
	"fmt"
	"math"
	"math/rand"
	"net/url"
	"strconv"
	"time"
)

func Round2(f float64) float64 { return math.Round(f*100) / 100 }
func F2(f float64) string      { return fmt.Sprintf("%.2f", f) }

func Atoi(s string, d int) int {
	if n, err := strconv.Atoi(s); err == nil { return n }
	return d
}

func RandomSlug(n int) string {
	const chars = "abcdefghijklmnopqrstuvwxyz0123456789"
	rand.Seed(time.Now().UnixNano())
	b := make([]byte, n)
	for i := range b { b[i] = chars[rand.Intn(len(chars))] }
	return string(b)
}

var counter = 10000
func NextBillNo() string {
	counter++
	yr := time.Now().Year()
	return fmt.Sprintf("CF-%d-%06d", yr, counter)
}

func URLEncode(s string) string { return url.QueryEscape(s) }
