package services

import (
	"bytes"
	"context"
	"time"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

type Storage struct {
	Client *minio.Client
	Bucket string
}

func NewStorage(endpoint, access, secret string, useSSL bool, bucket string) (*Storage, error) {
	cl, err := minio.New(endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(access, secret, ""),
		Secure: useSSL,
	})
	if err != nil {
		return nil, err
	}
	ctx := context.Background()
	exists, err := cl.BucketExists(ctx, bucket)
	if err == nil && !exists {
		_ = cl.MakeBucket(ctx, bucket, minio.MakeBucketOptions{})
	}
	return &Storage{Client: cl, Bucket: bucket}, nil
}

func (s *Storage) UploadPDF(ctx context.Context, key string, buf *bytes.Buffer) error {
	_, err := s.Client.PutObject(
		ctx, s.Bucket, key,
		bytes.NewReader(buf.Bytes()),
		int64(buf.Len()),
		minio.PutObjectOptions{ContentType: "application/pdf"},
	)
	return err
}

func (s *Storage) Presign(ctx context.Context, key string, expiry time.Duration) (string, error) {
	url, err := s.Client.PresignedGetObject(ctx, s.Bucket, key, expiry, nil)
	if err != nil {
		return "", err
	}
	return url.String(), nil
}
