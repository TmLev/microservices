package notifiers

type Message struct {
	Recipient  string  `json:"recipient"`
	Subject    string  `json:"subject"`
	Body       string  `json:"body"`
	RetryCount float64 `json:"retry_count"`
}

type Sender interface {
	Send(message *Message) bool
}
