package sms

import (
	"net/http"
	"net/url"
	"notifications/notifiers"

	log "github.com/sirupsen/logrus"
)

type Sender struct {
	apiID string
}

func NewSender() *Sender {
	return &Sender{
		apiID: "BD126304-AC4D-19AA-C9B4-F5C3F2F0E9EC",
	}
}

func (sender *Sender) Send(message *notifiers.Message) (returnToQueue bool) {
	log.Info("sms.Sender is trying to send SMS")

	u, err := url.Parse("https://sms.ru/sms/send")
	if err != nil {
		log.WithError(err).Warning("Error parsing url")
		return true
	}

	q := u.Query()
	q.Add("api_id", sender.apiID)
	q.Add("to", message.Recipient)
	q.Add("msg", message.Body)
	q.Add("json", "1")

	u.RawQuery = q.Encode()

	resp, _ := http.Get(u.String())

	log.Info("sms.Sender has (probably) sent SMS")

	returnToQueue = resp.StatusCode != 200
	if returnToQueue {
		log.Warning("Error occurred while sending")
	}

	return returnToQueue
}
