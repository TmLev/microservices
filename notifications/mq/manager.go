package mq

import (
	"fmt"
	"time"

	"github.com/streadway/amqp"

	log "github.com/sirupsen/logrus"

	"notifications/config"
	"notifications/notifiers"
)

type Manager struct {
	queueName string
	sender    notifiers.Sender
	consumer  *Consumer
	producer  *Producer
}

func NewManager(queueName string, sender notifiers.Sender) *Manager {
	return &Manager{
		queueName: queueName,
		sender:    sender,
		consumer:  &Consumer{},
		producer:  NewProducer(queueName),
	}
}

func (manager *Manager) Start(cfg *config.Config) {
	log.Print("Manager is trying to connect")

	var connection *amqp.Connection
	dialURL := makeDialURL(cfg)

	for {
		var err error
		connection, err = amqp.Dial(dialURL)
		if err == nil {
			break
		}

		log.WithError(err)
	}
	defer func() { _ = connection.Close() }()

	manager.Work(connection)
}

func (manager *Manager) Work(connection *amqp.Connection) {
	log.Print("Manager is starting to work")

	channel, err := connection.Channel()
	if err != nil {
		log.WithError(err).Fatal("Failed to get connection channel")
	}
	defer func() { _ = channel.Close() }()

	manager.producer.channel = channel

	queue, err := channel.QueueDeclare(
		manager.queueName,
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.WithError(err).Fatalf("Failed to declare queue %v", manager.queueName)
	}

	queueMessages, err := channel.Consume(
		queue.Name,
		"notifications",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.WithError(err).Fatalf("Failed to consume from %v queue", manager.queueName)
	}

	log.Print("Manager started eternity loop")

	for {
		message := manager.consumer.Consume(queueMessages)
		returnToQueue := manager.sender.Send(message)
		if returnToQueue {
			manager.producer.Produce(message)
		}

		time.Sleep(time.Second / 5)
	}
}

func makeDialURL(cfg *config.Config) string {
	return fmt.Sprintf(
		"amqp://%s:%s@%s:%s",
		cfg.MQUser,
		cfg.MQPassword,
		cfg.MQHost,
		cfg.MQPort,
	)
}
