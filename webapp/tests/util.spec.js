import { slugify, getFormattedDate, convertNewLinesToBR, CONSTANT } from '../src/util';
import { expect, test, describe } from 'vitest'

describe('slugify', () => {
  test('should return an empty string for an empty input', () => {
    expect(slugify('')).toBe('');
  });

  test('should return an empty string for a string with only spaces', () => {
    expect(slugify('   ')).toBe('');
  });

  test('should replace spaces and non-word characters with hyphens', () => {
    expect(slugify('Hello world!')).toBe('hello-world');
    expect(slugify('foo&bar')).toBe('foobar');
  });

  test('should replace multiple consecutive hyphens with a single hyphen', () => {
    expect(slugify('foo--bar')).toBe('foo-bar');
  });

  test('should not have extra hyphens at the start or end', () => {
    expect(slugify('-foo-bar-')).toBe('foo-bar');
  });
});

describe('getFormattedDate', () => {
  test('should return a formatted date string', () => {
    const formattedDate = getFormattedDate();
    expect(typeof formattedDate).toBe('string');
    console.log(formattedDate);
    console.log(formattedDate.split(':').length)
    expect(formattedDate.split(':').length).toBe(5);
  });

  test('should return the current date and time', () => {
    const currentDate = new Date();
    const formattedDate = getFormattedDate();
    const [day, month, year] = formattedDate.split(' ')[0].split(':');
    const [hour, minutes, seconds] = formattedDate.split(' ')[1].split(':');
    expect(day).toBe(String(currentDate.getDate()).padStart(2, '0'));
    expect(month).toBe(String(currentDate.getMonth() + 1).padStart(2, '0'));
    expect(year).toBe(String(currentDate.getFullYear()));
    expect(hour).toBe(String(currentDate.getHours()).padStart(2, '0'));
    expect(minutes).toBe(String(currentDate.getMinutes()).padStart(2, '0'));
    expect(seconds).toBe(String(currentDate.getSeconds()).padStart(2, '0'));
  });
});

describe('convertNewLinesToBR', () => {
  test('should replace newline characters with <br> tags', () => {
    const input = 'Hello\nWorld';
    const expected = 'Hello<br>World';
    expect(convertNewLinesToBR(input)).toEqual(expected);
  });

  test('should not modify input if there are no newline characters', () => {
    const input = 'Hello World';
    const expected = 'Hello World';
    expect(convertNewLinesToBR(input)).toEqual(expected);
  });

  test('should handle input with multiple newline characters correctly', () => {
    const input = 'Hello\nWorld\n';
    const expected = 'Hello<br>World<br>';
    expect(convertNewLinesToBR(input)).toEqual(expected);
  });

  test('should handle input with leading and trailing whitespace correctly', () => {
    const input = '  Hello\nWorld  ';
    const expected = '  Hello<br>World  ';
    expect(convertNewLinesToBR(input)).toEqual(expected);
  });
});

describe('DEFAULT_AUDIO_MOTION_OPTIONS', () => {
  test('should have the correct default values', () => {
    const options = CONSTANT.DEFAULT_AUDIO_MOTION_OPTIONS;

    expect(options.mode).toBe(10);
    expect(options.bgAlpha).toBe(0.7);
    expect(options.fillAlpha).toBe(0.6);
    expect(options.gradient).toBe('steelblue');
    expect(options.lineWidth).toBe(2);
    expect(options.lumiBars).toBe(false);
    expect(options.maxFreq).toBe(16000);
    expect(options.radial).toBe(false);
    expect(options.reflexAlpha).toBe(1);
    expect(options.linearAmplitude).toBe(true);
    expect(options.linearBoost).toBe(1.5);
    expect(options.reflexBright).toBe(1);
    expect(options.reflexRatio).toBe(0.5);
    expect(options.showScaleX).toBe(false);
    expect(options.showBgColor).toBe(false);
    expect(options.roundBars).toBe(true);
    expect(options.showPeaks).toBe(false);
    expect(options.moothing).toBe(0.8);
    expect(options.overlay).toBe(true);
  });
});