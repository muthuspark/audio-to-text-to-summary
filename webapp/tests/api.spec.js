import { getSummaries, API, payload, getSummaryById, removeSummary, updateRecordingName } from '../src/api'
import { expect, test, describe } from 'vitest'
import jest from 'jest-mock'

describe('getSummaries', () => {
    test('should return the response data when the request is successful', async () => {
        // Mock the fetch function to return a successful response
        global.fetch = jest.fn().mockResolvedValue({
            json: jest.fn().mockResolvedValue({ data: 'response data' }),
        });

        // Call the getSummaries function
        const result = await getSummaries();

        // Assert that the response data is returned
        expect(result).toEqual({ data: 'response data' });
        expect(global.fetch).toHaveBeenCalledWith(API.GET_SUMMARIES, payload({}));
    });

    test('should throw an error when the request fails', async () => {
        // Mock the fetch function to throw an error
        global.fetch = jest.fn().mockRejectedValue(new Error('Request failed'));

        // Call the getSummaries function and expect it to throw an error
        await expect(getSummaries()).rejects.toThrow('Request failed');
        expect(global.fetch).toHaveBeenCalledWith(API.GET_SUMMARIES, payload({}));
    });
});

describe('getSummaryById', () => {
    test('should return the summary data when the request is successful', async () => {
        // Mock the fetch function to return a successful response
        global.fetch = jest.fn().mockResolvedValue({
            json: jest.fn().mockResolvedValue({ data: 'summary data' }),
        });

        // Call the getSummaryById function
        const result = await getSummaryById('123');

        // Assert that the summary data is returned
        expect(result).toEqual({ data: 'summary data' });
        expect(global.fetch).toHaveBeenCalledWith(API.GET_SUMMARY, payload({ "id": '123' }));
    });

    test('should throw an error when the request fails', async () => {
        // Mock the fetch function to throw an error
        global.fetch = jest.fn().mockRejectedValue(new Error('Request failed'));

        // Call the getSummaryById function and expect it to throw an error
        await expect(getSummaryById('123')).rejects.toThrow('Request failed');
        expect(global.fetch).toHaveBeenCalledWith(API.GET_SUMMARY, payload({ "id": '123' }));
    });
});


describe('removeSummary', () => {
    test('should remove the summary and return the response data when the request is successful', async () => {
        // Mock the fetch function to return a successful response
        global.fetch = jest.fn().mockResolvedValue({
            json: jest.fn().mockResolvedValue({ data: 'response data' }),
        });

        // Call the removeSummary function
        const result = await removeSummary('audio_file_name');

        // Assert that the summary is removed and the response data is returned
        expect(result).toEqual({ data: 'response data' });
        expect(global.fetch).toHaveBeenCalledWith(API.REMOVE_SUMMARY, payload({ "audio_file_name": 'audio_file_name' }));
    });

    test('should throw an error when the request fails', async () => {
        // Mock the fetch function to throw an error
        global.fetch = jest.fn().mockRejectedValue(new Error('Request failed'));

        // Call the removeSummary function and expect it to throw an error
        await expect(removeSummary('audio_file_name')).rejects.toThrow('Request failed');
        expect(global.fetch).toHaveBeenCalledWith(API.REMOVE_SUMMARY, payload({ "audio_file_name": 'audio_file_name' }));
    });
});

describe('updateRecordingName', () => {
    test('should update the recording name and return the response data when the request is successful', async () => {
        // Mock the fetch function to return a successful response
        global.fetch = jest.fn().mockResolvedValue({
            json: jest.fn().mockResolvedValue({ data: 'response data' }),
        });

        // Call the updateRecordingName function
        const result = await updateRecordingName('new name', 'audio_file_name');

        // Assert that the recording name is updated and the response data is returned
        expect(result).toEqual({ data: 'response data' });
        expect(global.fetch).toHaveBeenCalledWith(API.UPDATE_TITLE, payload({
            "audio_file_name": 'audio_file_name',
            "recording_name": 'new name'
        }));
    });

    test('should throw an error when the request fails', async () => {
        // Mock the fetch function to throw an error
        global.fetch = jest.fn().mockRejectedValue(new Error('Request failed'));

        // Call the updateRecordingName function and expect it to throw an error
        await expect(updateRecordingName('new name', 'audio_file_name')).rejects.toThrow('Request failed');
        expect(global.fetch).toHaveBeenCalledWith(API.UPDATE_TITLE, payload({
            "audio_file_name": 'audio_file_name',
            "recording_name": 'new name'
        }));
    });
});