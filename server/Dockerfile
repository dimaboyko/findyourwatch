FROM ruby:2.6.5-alpine3.10
RUN apk add --no-cache build-base postgresql postgresql-dev libpq

WORKDIR /app

COPY . /app

RUN gem install bundler

RUN bundle install -j $(nproc) --quiet

EXPOSE 2300

