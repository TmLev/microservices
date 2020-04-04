package mq

import (
	"encoding/json"

	log "github.com/sirupsen/logrus"

	"github.com/streadway/amqp"

	"notifications/notifiers"
)

type Producer struct {
	queueName string
	channel   *amqp.Channel
}

func NewProducer(queueName string) *Producer {
	return &Producer{
		queueName: queueName,
	}
}

func (producer *Producer) Produce(message *notifiers.Message) {
	log.Info("Producer is trying to return message")

	body, err := json.Marshal(message)
	if err != nil {
		log.WithError(err).Warning("[Producer] JSON marshal failed, message won't be returned to queue")
		return
	}

	queueMessage := amqp.Publishing{
		ContentType: "application/json",
		Body:        []byte(body),
	}

	err = producer.channel.Publish(
		"",
		producer.queueName,
		false,
		false,
		queueMessage,
	)

	log.Info("Producer has (probably) returned message")

	if err != nil {
		log.WithError(err).Warning("Error occurred while returning message")
	}
}
