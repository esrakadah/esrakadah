#!/usr/bin/env bash
# Builds the round portrait and the rounded stage photo strip in assets/apple/.
# Usage: tools/build_photos.sh <Esra-Kadah-Portfolio checkout>
# Needs ImageMagick 7 (magick) and cwebp.
set -euo pipefail

portfolio_dir="${1:?path to the Esra-Kadah-Portfolio checkout}"
repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
output_dir="$repo_dir/assets/apple"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

portrait_size=320
tile_size=520
tile_gap=24
tile_radius=36

rounded_square() {
  local source="$1" target="$2" radius="$3" size="$4"
  magick "$source" -resize "${size}x${size}^" -gravity center -extent "${size}x${size}" \
    \( -size "${size}x${size}" xc:none -fill white \
       -draw "roundrectangle 0,0 $((size - 1)),$((size - 1)) $radius,$radius" \) \
    -alpha set -compose DstIn -composite "$target"
}

rounded_square "$repo_dir/assets/esra-kadah-headshot-2025.webp" "$work_dir/portrait.png" \
  $((portrait_size / 2)) "$portrait_size"
cwebp -quiet -q 86 -alpha_q 100 "$work_dir/portrait.png" -o "$output_dir/portrait.webp"

stage_photos=(build-with-gemini-2026 devfest-istanbul-2025 flutter-connection-2024)
for photo in "${stage_photos[@]}"; do
  rounded_square "$portfolio_dir/public/stage/$photo.webp" "$work_dir/$photo.png" "$tile_radius" "$tile_size"
done
magick -background none \
  "$work_dir/${stage_photos[0]}.png" \
  \( -size "${tile_gap}x${tile_size}" xc:none \) \
  "$work_dir/${stage_photos[1]}.png" \
  \( -size "${tile_gap}x${tile_size}" xc:none \) \
  "$work_dir/${stage_photos[2]}.png" \
  +append "$work_dir/strip.png"
cwebp -quiet -q 82 -alpha_q 100 "$work_dir/strip.png" -o "$output_dir/stage-strip.webp"

card_width=640
card_height=360
card_radius=24

rounded_card() {
  local source="$1" target="$2" gravity="$3"
  magick "$source" -resize "${card_width}x${card_height}^" -gravity "$gravity" \
    -extent "${card_width}x${card_height}" \
    \( -size "${card_width}x${card_height}" xc:none -fill white \
       -draw "roundrectangle 0,0 $((card_width - 1)),$((card_height - 1)) $card_radius,$card_radius" \) \
    -alpha set -compose DstIn -composite "$work_dir/card.png"
  cwebp -quiet -q 82 -alpha_q 100 "$work_dir/card.png" -o "$output_dir/$target.webp"
}

media_dir="$portfolio_dir/public/media"
rounded_card "$media_dir/backyard-barista-counter.webp" card-backyard-barista north
rounded_card "$media_dir/devto-genkit-dart-agent-approval.webp" card-genkit-agent center
rounded_card "$media_dir/fcaic-stream.webp" card-fcaic center
rounded_card "$media_dir/flutter-vibes-only-workshop.webp" card-vibes-workshop center
rounded_card "$media_dir/devto-flutter-web-budget-zero.webp" card-budget-zero center
rounded_card "$media_dir/devto-genkit-interrupt-restart.webp" card-genkit-restart center
rounded_card "$media_dir/fcaic-keynote-slide.webp" card-fcaic-keynote center
rounded_card "$media_dir/flutter-berlin-meetup.webp" card-flutter-berlin center

magick -size "${card_width}x${card_height}" xc:'#1c1c1e' \
  \( "$media_dir/flutter-design-patterns-cover.webp" -resize "x$((card_height - 48))" \) \
  -gravity center -composite "$work_dir/book-canvas.png"
rounded_card "$work_dir/book-canvas.png" card-book center
