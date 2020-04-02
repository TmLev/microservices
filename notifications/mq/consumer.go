package mq

import (
	"encoding/json"
	"time"

	"github.com/streadway/amqp"

	log "github.com/sirupsen/logrus"

	"notifications/notifiers"
)

type Consumer struct {
}

func (consumer *Consumer) Consume(queueMessages <-chan amqp.Delivery) *notifiers.Message {
	queueMessage := <-queueMessages
	body := queueMessage.Body

	var message notifiers.Message
	err := json.Unmarshal(body, &message)
	if err != nil {
		log.WithError(err).Warning("[Consumer] JSON unmarshal failed, skipping message")
	}

	log.WithField(
		"consumed_from",
		"email_queue",
	).WithTime(
		time.Now(),
	).Info(message)

	return &message
}
