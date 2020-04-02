package config

import (
	"github.com/caarlos0/env/v6"
	log "github.com/sirupsen/logrus"
)

type Config struct {
	MailHost           string   `env:"MAIL_HOST"`
	MailPort           int      `env:"MAIL_PORT"`
	MailSenderEmail    string   `env:"MAIL_SENDER_EMAIL"`
	MailSenderPassword string   `env:"MAIL_SENDER_PASSWORD"`
	Queues             []string `env:"NOTIFICATION_QUEUES" envSeparator:","`
	MQUser             string   `env:"RABBITMQ_USER"`
	MQPassword         string   `env:"RABBITMQ_PASS"`
	MQHost             string   `env:"MQ_HOST"`
	MQPort             string   `env:"MQ_PORT"`
}

func ParseEnvConfig() *Config {
	var config Config

	err := env.Parse(&config)
	if err != nil {
		log.WithError(err).Fatal("Failed to parse config")
	}

	return &config
}
