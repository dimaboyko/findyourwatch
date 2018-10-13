FROM ruby:2.5.1-alpine

RUN apk add --no-cache build-base postgresql postgresql-dev libpq

WORKDIR /app

COPY . /app

RUN gem install bundler

RUN bundle install -j $(nproc) --quiet

EXPOSE 2300

# ENTRYPOINT ["bundle", "exec"]
